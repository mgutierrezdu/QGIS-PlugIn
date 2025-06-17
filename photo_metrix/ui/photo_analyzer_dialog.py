from qgis.PyQt.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                                 QLabel, QFileDialog, QSpinBox, QDoubleSpinBox,
                                 QTextEdit, QGroupBox, QCheckBox, QComboBox,
                                 QProgressBar, QMessageBox, QTabWidget)
from qgis.PyQt.QtCore import Qt, QThread, pyqtSignal
from qgis.PyQt.QtGui import QPixmap, QPainter, QPen, QColor
import os
from ..distance_calculator import PhotoAnalyzer

class AnalysisWorker(QThread):
    """Worker para análisis en segundo plano"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    
    def __init__(self, image_path, analysis_type, reference_distance=None, reference_points=None):
        super().__init__()
        self.image_path = image_path
        self.analysis_type = analysis_type
        self.reference_distance = reference_distance
        self.reference_points = reference_points
        
    def run(self):
        try:
            self.progress.emit(10)
            analyzer = PhotoAnalyzer()
            
            self.progress.emit(30)
            if self.analysis_type == "advanced":
                result = analyzer.analyze_image_advanced(
                    self.image_path, 
                    self.reference_distance, 
                    self.reference_points
                )
            else:
                result = analyzer.analyze_image(self.image_path)
                
            self.progress.emit(100)
            self.finished.emit(result)
            
        except Exception as e:
            self.error.emit(str(e))

class PhotoAnalyzerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Photo Metrix - Analizador de Distancias")
        self.setMinimumSize(800, 600)
        self.image_path = None
        self.analysis_result = None
        self.reference_points = []
        
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Tabs para diferentes funcionalidades
        self.tab_widget = QTabWidget()
        
        # Tab 1: Análisis Básico
        self.setup_basic_tab()
        
        # Tab 2: Análisis Avanzado
        self.setup_advanced_tab()
        
        # Tab 3: Calibración Manual
        self.setup_calibration_tab()
        
        # Tab 4: Resultados
        self.setup_results_tab()
        
        layout.addWidget(self.tab_widget)
        
        # Botones de control
        button_layout = QHBoxLayout()
        self.analyze_btn = QPushButton("Analizar Imagen")
        self.analyze_btn.clicked.connect(self.analyze_image)
        self.close_btn = QPushButton("Cerrar")
        self.close_btn.clicked.connect(self.close)
        
        button_layout.addWidget(self.analyze_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.setLayout(layout)
        
    def setup_basic_tab(self):
        basic_widget = QVBoxLayout()
        
        # Selección de imagen
        image_group = QGroupBox("Selección de Imagen")
        image_layout = QVBoxLayout()
        
        self.image_label = QLabel("No se ha seleccionado ninguna imagen")
        self.image_label.setMinimumHeight(200)
        self.image_label.setStyleSheet("border: 2px dashed #ccc;")
        self.image_label.setAlignment(Qt.AlignCenter)
        
        self.select_image_btn = QPushButton("Seleccionar Imagen")
        self.select_image_btn.clicked.connect(self.select_image)
        
        image_layout.addWidget(self.image_label)
        image_layout.addWidget(self.select_image_btn)
        image_group.setLayout(image_layout)
        
        basic_widget.addWidget(image_group)
        
        # Opciones de análisis
        options_group = QGroupBox("Opciones de Análisis")
        options_layout = QVBoxLayout()
        
        self.confidence_spin = QDoubleSpinBox()
        self.confidence_spin.setRange(0.1, 1.0)
        self.confidence_spin.setValue(0.5)
        self.confidence_spin.setSingleStep(0.1)
        
        options_layout.addWidget(QLabel("Umbral de Confianza:"))
        options_layout.addWidget(self.confidence_spin)
        
        self.use_gps_check = QCheckBox("Usar metadatos GPS si están disponibles")
        self.use_gps_check.setChecked(True)
        options_layout.addWidget(self.use_gps_check)
        
        options_group.setLayout(options_layout)
        basic_widget.addWidget(options_group)
        
        basic_widget.addStretch()
        
        # Crear widget contenedor
        basic_container = QWidget()
        basic_container.setLayout(basic_widget)
        self.tab_widget.addTab(basic_container, "Análisis Básico")
        
    def setup_advanced_tab(self):
        advanced_widget = QVBoxLayout()
        
        # Configuración de cámara
        camera_group = QGroupBox("Configuración de Cámara")
        camera_layout = QVBoxLayout()
        
        self.focal_length_spin = QDoubleSpinBox()
        self.focal_length_spin.setRange(10, 500)
        self.focal_length_spin.setValue(35)
        self.focal_length_spin.setSuffix(" mm")
        
        self.sensor_width_spin = QDoubleSpinBox()
        self.sensor_width_spin.setRange(10, 50)
        self.sensor_width_spin.setValue(23.5)
        self.sensor_width_spin.setSuffix(" mm")
        
        camera_layout.addWidget(QLabel("Distancia Focal:"))
        camera_layout.addWidget(self.focal_length_spin)
        camera_layout.addWidget(QLabel("Ancho del Sensor:"))
        camera_layout.addWidget(self.sensor_width_spin)
        
        camera_group.setLayout(camera_layout)
        advanced_widget.addWidget(camera_group)
        
        # Métodos de calibración
        calibration_group = QGroupBox("Métodos de Calibración")
        calibration_layout = QVBoxLayout()
        
        self.calibration_combo = QComboBox()
        self.calibration_combo.addItems([
            "Automático (mejor disponible)",
            "GPS + Altitud",
            "Distancia de Referencia",
            "Estimación por Edificios"
        ])
        
        calibration_layout.addWidget(QLabel("Método de Calibración:"))
        calibration_layout.addWidget(self.calibration_combo)
        
        calibration_group.setLayout(calibration_layout)
        advanced_widget.addWidget(calibration_group)
        
        advanced_widget.addStretch()
        
        # Crear widget contenedor
        advanced_container = QWidget()
        advanced_container.setLayout(advanced_widget)
        self.tab_widget.addTab(advanced_container, "Análisis Avanzado")
        
    def setup_calibration_tab(self):
        calibration_widget = QVBoxLayout()
        
        # Instrucciones
        instructions = QLabel(
            "Para calibrar manualmente:\n"
            "1. Selecciona dos puntos en la imagen\n"
            "2. Ingresa la distancia real entre ellos\n"
            "3. Usa esta calibración para mediciones precisas"
        )
        instructions.setWordWrap(True)
        calibration_widget.addWidget(instructions)
        
        # Distancia de referencia
        ref_group = QGroupBox("Distancia de Referencia")
        ref_layout = QVBoxLayout()
        
        self.reference_distance_spin = QDoubleSpinBox()
        self.reference_distance_spin.setRange(0.1, 1000)
        self.reference_distance_spin.setValue(10)
        self.reference_distance_spin.setSuffix(" metros")
        
        ref_layout.addWidget(QLabel("Distancia Real:"))
        ref_layout.addWidget(self.reference_distance_spin)
        
        self.set_reference_btn = QPushButton("Establecer Puntos de Referencia")
        self.set_reference_btn.clicked.connect(self.set_reference_points)
        ref_layout.addWidget(self.set_reference_btn)
        
        ref_group.setLayout(ref_layout)
        calibration_widget.addWidget(ref_group)
        
        calibration_widget.addStretch()
        
        # Crear widget contenedor
        calibration_container = QWidget()
        calibration_container.setLayout(calibration_widget)
        self.tab_widget.addTab(calibration_container, "Calibración Manual")
        
    def setup_results_tab(self):
        results_widget = QVBoxLayout()
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setPlaceholderText("Los resultados del análisis aparecerán aquí...")
        
        results_widget.addWidget(self.results_text)
        
        # Crear widget contenedor
        results_container = QWidget()
        results_container.setLayout(results_widget)
        self.tab_widget.addTab(results_container, "Resultados")
        
    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar Imagen", "", 
            "Imágenes (*.jpg *.jpeg *.png *.tiff *.bmp)"
        )
        
        if file_path:
            self.image_path = file_path
            self.display_image(file_path)
            
    def display_image(self, image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            # Escalar la imagen para mostrar en el label
            scaled_pixmap = pixmap.scaled(
                300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setText("")
        else:
            self.image_label.setText("Error al cargar la imagen")
            
    def set_reference_points(self):
        if not self.image_path:
            QMessageBox.warning(self, "Error", "Primero selecciona una imagen")
            return
            
        # Aquí implementarías la selección de puntos en la imagen
        # Por ahora, usamos puntos simulados
        self.reference_points = [(100, 100), (300, 200)]
        QMessageBox.information(self, "Puntos de Referencia", 
                              "Puntos de referencia establecidos")
        
    def analyze_image(self):
        if not self.image_path:
            QMessageBox.warning(self, "Error", "Primero selecciona una imagen")
            return
            
        # Configurar worker
        analysis_type = "advanced" if self.tab_widget.currentIndex() > 0 else "basic"
        
        self.worker = AnalysisWorker(
            self.image_path,
            analysis_type,
            self.reference_distance_spin.value() if self.reference_points else None,
            self.reference_points
        )
        
        self.worker.finished.connect(self.on_analysis_finished)
        self.worker.error.connect(self.on_analysis_error)
        self.worker.progress.connect(self.progress_bar.setValue)
        
        # Mostrar progreso
        self.progress_bar.setVisible(True)
        self.analyze_btn.setEnabled(False)
        
        self.worker.start()
        
    def on_analysis_finished(self, result):
        self.analysis_result = result
        self.progress_bar.setVisible(False)
        self.analyze_btn.setEnabled(True)
        
        # Mostrar resultados
        self.display_results(result)
        
        # Cambiar a tab de resultados
        self.tab_widget.setCurrentIndex(3)
        
    def on_analysis_error(self, error_msg):
        self.progress_bar.setVisible(False)
        self.analyze_btn.setEnabled(True)
        QMessageBox.critical(self, "Error de Análisis", error_msg)
        
    def display_results(self, result):
        if isinstance(result, dict):
            # Resultado avanzado
            text = "=== RESULTADOS DEL ANÁLISIS ===\n\n"
            
            if 'distances' in result:
                text += "DISTANCIAS CALCULADAS:\n"
                for method, distance in result['distances'].items():
                    text += f"• {method}: {distance:.2f} metros\n"
                    
            if 'metadata' in result and result['metadata']:
                text += f"\nMETADATOS GPS:\n"
                text += f"• Latitud: {result['metadata']['lat']:.6f}\n"
                text += f"• Longitud: {result['metadata']['lon']:.6f}\n"
                text += f"• Altitud: {result['metadata']['altitude']} m\n"
                
            if 'centers' in result:
                text += f"\nCENTROS DE OBJETOS:\n"
                for i, center in enumerate(result['centers']):
                    text += f"• Objeto {i+1}: ({center[0]:.1f}, {center[1]:.1f})\n"
                    
        else:
            # Resultado básico
            text = f"Distancia calculada: {result:.2f} metros"
            
        self.results_text.setText(text) 