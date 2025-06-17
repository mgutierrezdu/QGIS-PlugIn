# -*- coding: utf-8 -*-
"""
Unified Geolocator Dialog - Main Interface
Combines image geolocation and distance calculation in one interface
"""

from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog,
    QTextEdit, QGroupBox, QCheckBox, QComboBox, QProgressBar, QMessageBox,
    QTabWidget, QWidget, QSpinBox, QDoubleSpinBox, QLineEdit, QListWidget,
    QSplitter, QFrame, QGridLayout, QTableWidget, QTableWidgetItem
)
from qgis.PyQt.QtCore import Qt, QThread, pyqtSignal, QTimer
from qgis.PyQt.QtGui import QPixmap, QPainter, QPen, QColor, QFont
from qgis.core import (
    QgsProject, QgsPointXY, QgsGeometry, QgsFeature, QgsVectorLayer,
    QgsFields, QgsField, QgsRasterLayer, QgsCoordinateReferenceSystem,
    QgsCoordinateTransform, QgsDistanceArea
)
from qgis.gui import QgsMapCanvas
import os
import exifread
from PIL import Image
from PIL.ExifTags import TAGS
import math
import json
from datetime import datetime

class ImageProcessor(QThread):
    """Worker thread for processing images"""
    progress = pyqtSignal(int)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, folder_path, process_type):
        super().__init__()
        self.folder_path = folder_path
        self.process_type = process_type  # 'geolocate' or 'analyze'
        
    def run(self):
        try:
            results = []
            files = [f for f in os.listdir(self.folder_path) 
                    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff'))]
            
            for i, filename in enumerate(files):
                self.progress.emit(int((i / len(files)) * 100))
                file_path = os.path.join(self.folder_path, filename)
                
                if self.process_type == 'geolocate':
                    result = self.extract_gps_data(file_path, filename)
                    if result:
                        results.append(result)
                elif self.process_type == 'analyze':
                    result = self.analyze_image(file_path, filename)
                    if result:
                        results.append(result)
                        
            self.finished.emit({'type': self.process_type, 'results': results})
            
        except Exception as e:
            self.error.emit(str(e))
    
    def extract_gps_data(self, file_path, filename):
        """Extract GPS data from image"""
        try:
            with open(file_path, 'rb') as f:
                tags = exifread.process_file(f, stop_tag='GPS GPSLongitude')
                
            if "GPS GPSLatitude" in tags and "GPS GPSLongitude" in tags:
                lat = self._get_decimal_from_dms(
                    tags["GPS GPSLatitude"].values, 
                    tags["GPS GPSLatitudeRef"].values
                )
                lon = self._get_decimal_from_dms(
                    tags["GPS GPSLongitude"].values, 
                    tags["GPS GPSLongitudeRef"].values
                )
                
                return {
                    'filename': filename,
                    'path': file_path,
                    'lat': lat,
                    'lon': lon,
                    'has_gps': True
                }
            else:
                return {
                    'filename': filename,
                    'path': file_path,
                    'lat': None,
                    'lon': None,
                    'has_gps': False
                }
        except Exception as e:
            return {
                'filename': filename,
                'path': file_path,
                'lat': None,
                'lon': None,
                'has_gps': False,
                'error': str(e)
            }
    
    def analyze_image(self, file_path, filename):
        """Analyze image for distance calculation"""
        try:
            # Basic image analysis (placeholder for more advanced analysis)
            image = Image.open(file_path)
            width, height = image.size
            
            return {
                'filename': filename,
                'path': file_path,
                'width': width,
                'height': height,
                'size_mb': os.path.getsize(file_path) / (1024 * 1024)
            }
        except Exception as e:
            return {
                'filename': filename,
                'path': file_path,
                'error': str(e)
            }
    
    def _get_decimal_from_dms(self, dms, ref):
        """Convert DMS coordinates to decimal"""
        degrees = float(dms[0].num) / float(dms[0].den)
        minutes = float(dms[1].num) / float(dms[1].den)
        seconds = float(dms[2].num) / float(dms[2].den)
        decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
        if ref in ['S', 'W']:
            decimal = -decimal
        return decimal

class UnifiedGeolocatorDialog(QDialog):
    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface
        self.setWindowTitle("Unified Geolocator - Geolocalización y Análisis de Imágenes")
        self.setMinimumSize(1200, 800)
        
        # Data storage
        self.geolocated_images = []
        self.analyzed_images = []
        self.current_folder = ""
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main user interface"""
        layout = QVBoxLayout()
        
        # Main splitter
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Controls
        left_panel = self.create_left_panel()
        main_splitter.addWidget(left_panel)
        
        # Right panel - Results and Map
        right_panel = self.create_right_panel()
        main_splitter.addWidget(right_panel)
        
        # Set splitter proportions
        main_splitter.setSizes([400, 800])
        
        layout.addWidget(main_splitter)
        
        # Status bar
        self.status_label = QLabel("Listo para procesar imágenes")
        self.status_label.setStyleSheet("padding: 5px; background-color: #f0f0f0; border: 1px solid #ccc;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
    def create_left_panel(self):
        """Create the left control panel"""
        left_widget = QWidget()
        layout = QVBoxLayout()
        
        # Folder selection
        folder_group = QGroupBox("Selección de Carpeta")
        folder_layout = QVBoxLayout()
        
        self.folder_label = QLabel("No se ha seleccionado ninguna carpeta")
        self.folder_label.setWordWrap(True)
        self.folder_label.setStyleSheet("padding: 10px; background-color: #f9f9f9; border: 1px solid #ddd;")
        
        folder_btn_layout = QHBoxLayout()
        self.browse_btn = QPushButton("Examinar Carpeta")
        self.browse_btn.clicked.connect(self.browse_folder)
        self.clear_btn = QPushButton("Limpiar")
        self.clear_btn.clicked.connect(self.clear_data)
        
        folder_btn_layout.addWidget(self.browse_btn)
        folder_btn_layout.addWidget(self.clear_btn)
        
        folder_layout.addWidget(self.folder_label)
        folder_layout.addLayout(folder_btn_layout)
        folder_group.setLayout(folder_layout)
        layout.addWidget(folder_group)
        
        # Processing options
        options_group = QGroupBox("Opciones de Procesamiento")
        options_layout = QVBoxLayout()
        
        self.geolocate_check = QCheckBox("Geolocalizar imágenes")
        self.geolocate_check.setChecked(True)
        
        self.analyze_check = QCheckBox("Analizar imágenes para distancias")
        self.analyze_check.setChecked(True)
        
        self.add_basemap_check = QCheckBox("Agregar mapa base OpenStreetMap")
        self.add_basemap_check.setChecked(True)
        
        self.create_layer_check = QCheckBox("Crear capa vectorial en QGIS")
        self.create_layer_check.setChecked(True)
        
        options_layout.addWidget(self.geolocate_check)
        options_layout.addWidget(self.analyze_check)
        options_layout.addWidget(self.add_basemap_check)
        options_layout.addWidget(self.create_layer_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Process button
        self.process_btn = QPushButton("Procesar Imágenes")
        self.process_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.process_btn.clicked.connect(self.process_images)
        self.process_btn.setEnabled(False)
        layout.addWidget(self.process_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Export options
        export_group = QGroupBox("Exportar Resultados")
        export_layout = QVBoxLayout()
        
        export_btn_layout = QHBoxLayout()
        self.export_csv_btn = QPushButton("Exportar CSV")
        self.export_csv_btn.clicked.connect(self.export_csv)
        self.export_geojson_btn = QPushButton("Exportar GeoJSON")
        self.export_geojson_btn.clicked.connect(self.export_geojson)
        
        export_btn_layout.addWidget(self.export_csv_btn)
        export_btn_layout.addWidget(self.export_geojson_btn)
        
        export_layout.addLayout(export_btn_layout)
        export_group.setLayout(export_layout)
        layout.addWidget(export_group)
        
        layout.addStretch()
        left_widget.setLayout(layout)
        return left_widget
        
    def create_right_panel(self):
        """Create the right results panel"""
        right_widget = QWidget()
        layout = QVBoxLayout()
        
        # Tab widget for different views
        self.tab_widget = QTabWidget()
        
        # Tab 1: Results Table
        self.results_tab = self.create_results_tab()
        self.tab_widget.addTab(self.results_tab, "Resultados")
        
        # Tab 2: Map View
        self.map_tab = self.create_map_tab()
        self.tab_widget.addTab(self.map_tab, "Vista de Mapa")
        
        # Tab 3: Statistics
        self.stats_tab = self.create_stats_tab()
        self.tab_widget.addTab(self.stats_tab, "Estadísticas")
        
        layout.addWidget(self.tab_widget)
        right_widget.setLayout(layout)
        return right_widget
        
    def create_results_tab(self):
        """Create the results table tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(6)
        self.results_table.setHorizontalHeaderLabels([
            "Archivo", "Latitud", "Longitud", "GPS", "Análisis", "Estado"
        ])
        
        layout.addWidget(self.results_table)
        widget.setLayout(layout)
        return widget
        
    def create_map_tab(self):
        """Create the map view tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Map canvas
        self.map_canvas = QgsMapCanvas()
        self.map_canvas.setCanvasColor(Qt.white)
        
        layout.addWidget(self.map_canvas)
        widget.setLayout(layout)
        return widget
        
    def create_stats_tab(self):
        """Create the statistics tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        self.stats_text.setFont(QFont("Courier", 10))
        
        layout.addWidget(self.stats_text)
        widget.setLayout(layout)
        return widget
        
    def browse_folder(self):
        """Browse for folder containing images"""
        folder = QFileDialog.getExistingDirectory(
            self, 
            "Seleccionar carpeta con imágenes",
            ""
        )
        
        if folder:
            self.current_folder = folder
            self.folder_label.setText(f"Carpeta seleccionada:\n{folder}")
            self.process_btn.setEnabled(True)
            self.status_label.setText(f"Carpeta cargada: {len(os.listdir(folder))} archivos encontrados")
            
    def clear_data(self):
        """Clear all data"""
        self.current_folder = ""
        self.geolocated_images = []
        self.analyzed_images = []
        self.folder_label.setText("No se ha seleccionado ninguna carpeta")
        self.process_btn.setEnabled(False)
        self.results_table.setRowCount(0)
        self.stats_text.clear()
        self.status_label.setText("Datos limpiados")
        
    def process_images(self):
        """Process images in the selected folder"""
        if not self.current_folder:
            QMessageBox.warning(self, "Error", "Por favor selecciona una carpeta primero")
            return
            
        if not self.geolocate_check.isChecked() and not self.analyze_check.isChecked():
            QMessageBox.warning(self, "Error", "Selecciona al menos una opción de procesamiento")
            return
            
        # Start processing
        self.process_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Procesando imágenes...")
        
        # Create and start worker thread
        self.worker = ImageProcessor(self.current_folder, 'geolocate')
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self.on_processing_finished)
        self.worker.error.connect(self.on_processing_error)
        self.worker.start()
        
    def on_processing_finished(self, results):
        """Handle processing completion"""
        self.progress_bar.setVisible(False)
        self.process_btn.setEnabled(True)
        
        if results['type'] == 'geolocate':
            self.geolocated_images = results['results']
            self.update_results_table()
            self.update_statistics()
            
            if self.add_basemap_check.isChecked():
                self.add_osm_basemap()
                
            if self.create_layer_check.isChecked():
                self.create_qgis_layer()
                
        self.status_label.setText(f"Procesamiento completado: {len(results['results'])} imágenes procesadas")
        
    def on_processing_error(self, error_msg):
        """Handle processing errors"""
        self.progress_bar.setVisible(False)
        self.process_btn.setEnabled(True)
        self.status_label.setText(f"Error: {error_msg}")
        QMessageBox.critical(self, "Error", f"Error durante el procesamiento: {error_msg}")
        
    def update_results_table(self):
        """Update the results table with processed data"""
        self.results_table.setRowCount(len(self.geolocated_images))
        
        for i, image_data in enumerate(self.geolocated_images):
            self.results_table.setItem(i, 0, QTableWidgetItem(image_data['filename']))
            
            if image_data['has_gps']:
                self.results_table.setItem(i, 1, QTableWidgetItem(f"{image_data['lat']:.6f}"))
                self.results_table.setItem(i, 2, QTableWidgetItem(f"{image_data['lon']:.6f}"))
                self.results_table.setItem(i, 3, QTableWidgetItem("✓"))
            else:
                self.results_table.setItem(i, 1, QTableWidgetItem("N/A"))
                self.results_table.setItem(i, 2, QTableWidgetItem("N/A"))
                self.results_table.setItem(i, 3, QTableWidgetItem("✗"))
                
            self.results_table.setItem(i, 4, QTableWidgetItem("Pendiente"))
            self.results_table.setItem(i, 5, QTableWidgetItem("Completado"))
            
    def update_statistics(self):
        """Update statistics display"""
        total_images = len(self.geolocated_images)
        gps_images = sum(1 for img in self.geolocated_images if img['has_gps'])
        no_gps_images = total_images - gps_images
        
        stats_text = f"""
ESTADÍSTICAS DEL PROCESAMIENTO
==============================

Total de imágenes procesadas: {total_images}
Imágenes con datos GPS: {gps_images}
Imágenes sin datos GPS: {no_gps_images}
Porcentaje con GPS: {(gps_images/total_images*100):.1f}%

DETALLES POR ARCHIVO:
====================
"""
        
        for img in self.geolocated_images:
            status = "GPS ✓" if img['has_gps'] else "GPS ✗"
            stats_text += f"{img['filename']}: {status}\n"
            
        self.stats_text.setText(stats_text)
        
    def add_osm_basemap(self):
        """Add OpenStreetMap basemap to QGIS"""
        try:
            url = "type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png"
            layer = QgsRasterLayer(url, "OpenStreetMap", "wms")
            if layer.isValid():
                QgsProject.instance().addMapLayer(layer, False)
                QgsProject.instance().layerTreeRoot().insertLayer(0, layer)
                self.status_label.setText("Mapa base OpenStreetMap agregado")
            else:
                QMessageBox.warning(self, "Error", "No se pudo cargar el mapa base OpenStreetMap")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al cargar mapa base: {str(e)}")
            
    def create_qgis_layer(self):
        """Create QGIS vector layer with geolocated images"""
        try:
            # Create point layer
            layer = QgsVectorLayer("Point?crs=EPSG:4326", "Imágenes Geolocalizadas", "memory")
            pr = layer.dataProvider()
            
            # Add fields
            fields = QgsFields()
            fields.append(QgsField("archivo", QgsField.String))
            fields.append(QgsField("latitud", QgsField.Double))
            fields.append(QgsField("longitud", QgsField.Double))
            fields.append(QgsField("fecha_proc", QgsField.DateTime))
            
            pr.addAttributes(fields)
            layer.updateFields()
            
            # Add features for images with GPS data
            features = []
            for img_data in self.geolocated_images:
                if img_data['has_gps']:
                    feat = QgsFeature(layer.fields())
                    feat.setGeometry(QgsGeometry.fromPointXY(
                        QgsPointXY(img_data['lon'], img_data['lat'])
                    ))
                    feat.setAttribute("archivo", img_data['filename'])
                    feat.setAttribute("latitud", img_data['lat'])
                    feat.setAttribute("longitud", img_data['lon'])
                    feat.setAttribute("fecha_proc", datetime.now())
                    features.append(feat)
                    
            pr.addFeatures(features)
            layer.updateExtents()
            
            # Add to project
            QgsProject.instance().addMapLayer(layer)
            
            self.status_label.setText(f"Capa creada con {len(features)} puntos")
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al crear capa: {str(e)}")
            
    def export_csv(self):
        """Export results to CSV"""
        if not self.geolocated_images:
            QMessageBox.warning(self, "Error", "No hay datos para exportar")
            return
            
        filename, _ = QFileDialog.getSaveFileName(
            self, "Guardar CSV", "", "CSV Files (*.csv)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("Archivo,Latitud,Longitud,Tiene_GPS,Error\n")
                    for img in self.geolocated_images:
                        lat = f"{img['lat']:.6f}" if img['has_gps'] else "N/A"
                        lon = f"{img['lon']:.6f}" if img['has_gps'] else "N/A"
                        gps = "Sí" if img['has_gps'] else "No"
                        error = img.get('error', '')
                        f.write(f"{img['filename']},{lat},{lon},{gps},{error}\n")
                        
                QMessageBox.information(self, "Éxito", f"Archivo CSV guardado: {filename}")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al exportar CSV: {str(e)}")
                
    def export_geojson(self):
        """Export results to GeoJSON"""
        if not self.geolocated_images:
            QMessageBox.warning(self, "Error", "No hay datos para exportar")
            return
            
        filename, _ = QFileDialog.getSaveFileName(
            self, "Guardar GeoJSON", "", "GeoJSON Files (*.geojson)"
        )
        
        if filename:
            try:
                geojson = {
                    "type": "FeatureCollection",
                    "features": []
                }
                
                for img in self.geolocated_images:
                    if img['has_gps']:
                        feature = {
                            "type": "Feature",
                            "geometry": {
                                "type": "Point",
                                "coordinates": [img['lon'], img['lat']]
                            },
                            "properties": {
                                "filename": img['filename'],
                                "has_gps": True
                            }
                        }
                        geojson["features"].append(feature)
                        
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(geojson, f, indent=2, ensure_ascii=False)
                    
                QMessageBox.information(self, "Éxito", f"Archivo GeoJSON guardado: {filename}")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al exportar GeoJSON: {str(e)}") 