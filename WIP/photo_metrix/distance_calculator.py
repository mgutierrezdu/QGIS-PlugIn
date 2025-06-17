import cv2
from ultralytics import YOLO
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS
import math
from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject

class PhotoAnalyzer:
    def __init__(self):
        self.model = YOLO("model/yolov8n.pt")
        
    def get_image_metadata(self, image_path):
        """Extrae metadatos GPS de la imagen"""
        try:
            image = Image.open(image_path)
            exif = image._getexif()
            if exif is None:
                return None
                
            metadata = {}
            for tag_id in exif:
                tag = TAGS.get(tag_id, tag_id)
                data = exif.get(tag_id)
                metadata[tag] = data
                
            # Extraer coordenadas GPS
            if 'GPSInfo' in metadata:
                gps_info = metadata['GPSInfo']
                lat = self._convert_to_degrees(gps_info.get(2, [0, 0, 0]))
                lon = self._convert_to_degrees(gps_info.get(4, [0, 0, 0]))
                altitude = gps_info.get(6, 0)
                return {'lat': lat, 'lon': lon, 'altitude': altitude}
            return None
        except Exception as e:
            print(f"Error extrayendo metadatos: {e}")
            return None
    
    def _convert_to_degrees(self, dms):
        """Convierte coordenadas DMS a decimal"""
        degrees = dms[0]
        minutes = dms[1]
        seconds = dms[2]
        return degrees + (minutes / 60.0) + (seconds / 3600.0)
    
    def calculate_ground_resolution(self, focal_length, sensor_width, image_width, altitude):
        """Calcula la resolución del suelo en metros por píxel"""
        # Fórmula: GSD = (altura * sensor_width) / (focal_length * image_width)
        gsd = (altitude * sensor_width) / (focal_length * image_width)
        return gsd
    
    def analyze_image_advanced(self, image_path, reference_distance=None, reference_points=None):
        """Análisis avanzado con múltiples métodos de calibración"""
        # 1. Cargar imagen y ejecutar detección
        image = cv2.imread(image_path)
        results = self.model.predict(image)
        
        # 2. Obtener metadatos GPS
        metadata = self.get_image_metadata(image_path)
        
        # 3. Obtener bounding boxes
        boxes = results[0].boxes.xyxy.cpu().numpy()
        confidences = results[0].boxes.conf.cpu().numpy()
        classes = results[0].boxes.cls.cpu().numpy()
        
        if len(boxes) < 2:
            raise ValueError("Se necesitan al menos 2 objetos para calcular distancia")
        
        # 4. Filtrar por confianza
        high_conf_boxes = boxes[confidences > 0.5]
        if len(high_conf_boxes) < 2:
            high_conf_boxes = boxes[:2]  # Usar los primeros 2 si no hay suficientes con alta confianza
        
        # 5. Calcular distancias usando diferentes métodos
        distances = {}
        
        # Método 1: Distancia euclidiana en píxeles
        centro1 = ((high_conf_boxes[0][0] + high_conf_boxes[0][2]) / 2, 
                   (high_conf_boxes[0][1] + high_conf_boxes[0][3]) / 2)
        centro2 = ((high_conf_boxes[1][0] + high_conf_boxes[1][2]) / 2, 
                   (high_conf_boxes[1][1] + high_conf_boxes[1][3]) / 2)
        
        distancia_pixeles = np.sqrt((centro2[0] - centro1[0])**2 + (centro2[1] - centro1[1])**2)
        distances['pixels'] = distancia_pixeles
        
        # Método 2: Calibración con metadatos GPS
        if metadata and metadata['altitude']:
            # Valores típicos de cámara (ajustar según la cámara real)
            focal_length = 35  # mm
            sensor_width = 23.5  # mm (APS-C)
            image_width = image.shape[1]
            
            gsd = self.calculate_ground_resolution(
                focal_length, sensor_width, image_width, metadata['altitude']
            )
            distances['gps_calibrated'] = distancia_pixeles * gsd
        
        # Método 3: Calibración con distancia de referencia
        if reference_distance and reference_points:
            ref_pixels = np.sqrt(
                (reference_points[1][0] - reference_points[0][0])**2 + 
                (reference_points[1][1] - reference_points[0][1])**2
            )
            scale_factor = reference_distance / ref_pixels
            distances['reference_calibrated'] = distancia_pixeles * scale_factor
        
        # Método 4: Estimación basada en altura promedio de edificios
        building_height_estimate = 10  # metros (altura promedio)
        distances['building_estimate'] = distancia_pixeles * (building_height_estimate / 100)  # Aproximación
        
        return {
            'distances': distances,
            'centers': [centro1, centro2],
            'boxes': high_conf_boxes[:2],
            'metadata': metadata,
            'image_shape': image.shape
        }
    
    def analyze_image(self, image_path):
        """Método original simplificado para compatibilidad"""
        result = self.analyze_image_advanced(image_path)
        # Retornar la distancia más confiable disponible
        if 'gps_calibrated' in result['distances']:
            return result['distances']['gps_calibrated']
        elif 'reference_calibrated' in result['distances']:
            return result['distances']['reference_calibrated']
        else:
            return result['distances']['building_estimate']

# Función de compatibilidad
def analyze_image(image_path):
    analyzer = PhotoAnalyzer()
    return analyzer.analyze_image(image_path)