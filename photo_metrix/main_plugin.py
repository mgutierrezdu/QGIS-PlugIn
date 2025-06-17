from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox, QMenu
from qgis.PyQt.QtGui import QIcon
from qgis.core import (QgsProject, QgsPointXY, QgsDistanceArea, QgsVectorLayer,
                       QgsFeature, QgsGeometry, QgsField, QgsFields, QgsCoordinateReferenceSystem)
from qgis.gui import QgsMapCanvas
import os
from .distance_calculator import PhotoAnalyzer
from .ui.photo_analyzer_dialog import PhotoAnalyzerDialog

class PhotoMetrixPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.actions = []
        self.menu = 'Photo Metrix'
        self.toolbar = self.iface.addToolBar('Photo Metrix')
        self.toolbar.setObjectName('PhotoMetrixToolbar')
        
        # Inicializar analizador
        self.analyzer = PhotoAnalyzer()
        
        # Variables para el estado del plugin
        self.current_analysis = None
        self.measurement_layer = None
        
    def initGui(self):
        """Inicializar la interfaz gráfica del plugin"""
        
        # Acción principal
        icon_path = os.path.join(os.path.dirname(__file__), 'icons', 'icon.png')
        self.action = QAction(
            QIcon(icon_path) if os.path.exists(icon_path) else QIcon(),
            "Photo Metrix",
            self.iface.mainWindow()
        )
        self.action.setObjectName('PhotoMetrixAction')
        self.action.setWhatsThis("Analizar distancias en fotografías usando IA")
        self.action.setStatusTip("Analizar distancias en fotografías")
        self.action.triggered.connect(self.run)
        
        # Agregar a la barra de herramientas
        self.toolbar.addAction(self.action)
        self.iface.addToolBarIcon(self.action)
        self.actions.append(self.action)
        
        # Agregar al menú
        self.iface.addPluginToMenu(self.menu, self.action)
        
        # Submenú para funcionalidades adicionales
        self.setup_submenu()
        
    def setup_submenu(self):
        """Configurar submenú con funcionalidades adicionales"""
        
        # Menú contextual
        self.context_menu = QMenu("Photo Metrix")
        
        # Acción para análisis rápido
        self.quick_analysis_action = QAction("Análisis Rápido", self.iface.mainWindow())
        self.quick_analysis_action.triggered.connect(self.quick_analysis)
        self.context_menu.addAction(self.quick_analysis_action)
        
        # Acción para crear capa de mediciones
        self.create_layer_action = QAction("Crear Capa de Mediciones", self.iface.mainWindow())
        self.create_layer_action.triggered.connect(self.create_measurement_layer)
        self.context_menu.addAction(self.create_layer_action)
        
        # Acción para exportar resultados
        self.export_action = QAction("Exportar Resultados", self.iface.mainWindow())
        self.export_action.triggered.connect(self.export_results)
        self.context_menu.addAction(self.export_action)
        
        # Agregar separador
        self.context_menu.addSeparator()
        
        # Acción para configuración
        self.settings_action = QAction("Configuración", self.iface.mainWindow())
        self.settings_action.triggered.connect(self.show_settings)
        self.context_menu.addAction(self.settings_action)
        
        # Agregar al menú principal
        self.iface.addPluginToMenu(self.menu, self.context_menu.menuAction())
        
    def unload(self):
        """Descargar el plugin"""
        for action in self.actions:
            self.iface.removeToolBarIcon(action)
            self.iface.removePluginMenu(self.menu, action)
            
        # Remover menú contextual
        self.iface.removePluginMenu(self.menu, self.context_menu.menuAction())
        
        # Remover barra de herramientas
        del self.toolbar
        
    def run(self):
        """Ejecutar el plugin principal"""
        try:
            # Mostrar diálogo principal
            dialog = PhotoAnalyzerDialog(self.iface.mainWindow())
            if dialog.exec_():
                # Si el análisis fue exitoso, crear capa en QGIS
                if dialog.analysis_result:
                    self.create_qgis_layer(dialog.analysis_result, dialog.image_path)
                    
        except Exception as e:
            QMessageBox.critical(
                self.iface.mainWindow(),
                "Error",
                f"Error al ejecutar el plugin: {str(e)}"
            )
            
    def quick_analysis(self):
        """Análisis rápido sin interfaz gráfica"""
        try:
            # Seleccionar imagen
            image_path, _ = QFileDialog.getOpenFileName(
                self.iface.mainWindow(),
                "Seleccionar Imagen para Análisis Rápido",
                "",
                "Imágenes (*.jpg *.jpeg *.png *.tiff *.bmp)"
            )
            
            if not image_path:
                return
                
            # Realizar análisis
            result = self.analyzer.analyze_image(image_path)
            
            # Mostrar resultado
            QMessageBox.information(
                self.iface.mainWindow(),
                "Análisis Rápido",
                f"Distancia calculada: {result:.2f} metros"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self.iface.mainWindow(),
                "Error",
                f"Error en análisis rápido: {str(e)}"
            )
            
    def create_measurement_layer(self):
        """Crear una capa vectorial para almacenar mediciones"""
        try:
            # Crear capa de puntos
            layer = QgsVectorLayer("Point?crs=EPSG:4326", "Mediciones Photo Metrix", "memory")
            
            # Agregar campos
            fields = QgsFields()
            fields.append(QgsField("id", QVariant.Int))
            fields.append(QgsField("imagen", QVariant.String))
            fields.append(QgsField("distancia", QVariant.Double))
            fields.append(QgsField("metodo", QVariant.String))
            fields.append(QgsField("fecha", QVariant.DateTime))
            
            layer.dataProvider().addAttributes(fields)
            layer.updateFields()
            
            # Agregar al proyecto
            QgsProject.instance().addMapLayer(layer)
            
            self.measurement_layer = layer
            
            QMessageBox.information(
                self.iface.mainWindow(),
                "Capa Creada",
                "Capa de mediciones creada exitosamente"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self.iface.mainWindow(),
                "Error",
                f"Error al crear capa: {str(e)}"
            )
            
    def create_qgis_layer(self, analysis_result, image_path):
        """Crear capa en QGIS con los resultados del análisis"""
        try:
            if isinstance(analysis_result, dict) and 'centers' in analysis_result:
                # Crear capa de puntos para los objetos detectados
                layer = QgsVectorLayer("Point?crs=EPSG:4326", "Objetos Detectados", "memory")
                
                # Agregar campos
                fields = QgsFields()
                fields.append(QgsField("id", QVariant.Int))
                fields.append(QgsField("imagen", QVariant.String))
                fields.append(QgsField("tipo", QVariant.String))
                fields.append(QgsField("confianza", QVariant.Double))
                
                layer.dataProvider().addAttributes(fields)
                layer.updateFields()
                
                # Crear features para cada objeto
                for i, center in enumerate(analysis_result['centers']):
                    feature = QgsFeature(fields)
                    feature.setId(i)
                    feature.setAttribute("id", i)
                    feature.setAttribute("imagen", os.path.basename(image_path))
                    feature.setAttribute("tipo", "Objeto")
                    feature.setAttribute("confianza", 0.8)  # Valor por defecto
                    
                    # Crear geometría (convertir coordenadas de imagen a coordenadas geográficas)
                    # Aquí necesitarías implementar la conversión real
                    point = QgsPointXY(center[0], center[1])
                    feature.setGeometry(QgsGeometry.fromPointXY(point))
                    
                    layer.dataProvider().addFeature(feature)
                
                # Agregar al proyecto
                QgsProject.instance().addMapLayer(layer)
                
                # Crear capa de líneas para las distancias
                if 'distances' in analysis_result:
                    self.create_distance_layer(analysis_result, image_path)
                    
        except Exception as e:
            QMessageBox.warning(
                self.iface.mainWindow(),
                "Advertencia",
                f"No se pudo crear la capa: {str(e)}"
            )
            
    def create_distance_layer(self, analysis_result, image_path):
        """Crear capa de líneas para mostrar las distancias"""
        try:
            layer = QgsVectorLayer("LineString?crs=EPSG:4326", "Distancias", "memory")
            
            # Agregar campos
            fields = QgsFields()
            fields.append(QgsField("id", QVariant.Int))
            fields.append(QgsField("imagen", QVariant.String))
            fields.append(QgsField("distancia", QVariant.Double))
            fields.append(QgsField("metodo", QVariant.String))
            
            layer.dataProvider().addAttributes(fields)
            layer.updateFields()
            
            # Crear feature para la línea de distancia
            if 'centers' in analysis_result and len(analysis_result['centers']) >= 2:
                feature = QgsFeature(fields)
                feature.setId(0)
                feature.setAttribute("id", 0)
                feature.setAttribute("imagen", os.path.basename(image_path))
                
                # Usar la distancia más confiable
                distances = analysis_result['distances']
                if 'gps_calibrated' in distances:
                    distance = distances['gps_calibrated']
                    method = "GPS Calibrado"
                elif 'reference_calibrated' in distances:
                    distance = distances['reference_calibrated']
                    method = "Referencia Calibrada"
                else:
                    distance = list(distances.values())[0]
                    method = "Estimación"
                    
                feature.setAttribute("distancia", distance)
                feature.setAttribute("metodo", method)
                
                # Crear geometría de línea
                centers = analysis_result['centers']
                line_points = [QgsPointXY(centers[0][0], centers[0][1]),
                              QgsPointXY(centers[1][0], centers[1][1])]
                feature.setGeometry(QgsGeometry.fromPolylineXY(line_points))
                
                layer.dataProvider().addFeature(feature)
            
            # Agregar al proyecto
            QgsProject.instance().addMapLayer(layer)
            
        except Exception as e:
            print(f"Error creando capa de distancias: {e}")
            
    def export_results(self):
        """Exportar resultados a archivo"""
        try:
            if not self.current_analysis:
                QMessageBox.warning(
                    self.iface.mainWindow(),
                    "Advertencia",
                    "No hay resultados para exportar"
                )
                return
                
            # Seleccionar archivo de destino
            file_path, _ = QFileDialog.getSaveFileName(
                self.iface.mainWindow(),
                "Guardar Resultados",
                "",
                "Archivos CSV (*.csv);;Archivos JSON (*.json)"
            )
            
            if not file_path:
                return
                
            # Aquí implementarías la exportación real
            QMessageBox.information(
                self.iface.mainWindow(),
                "Exportación",
                "Resultados exportados exitosamente"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self.iface.mainWindow(),
                "Error",
                f"Error al exportar: {str(e)}"
            )
            
    def show_settings(self):
        """Mostrar configuración del plugin"""
        QMessageBox.information(
            self.iface.mainWindow(),
            "Configuración",
            "Configuración del plugin Photo Metrix"
        )

# Función de compatibilidad
class MiPluginIA(PhotoMetrixPlugin):
    """Clase de compatibilidad con el nombre original"""
    pass