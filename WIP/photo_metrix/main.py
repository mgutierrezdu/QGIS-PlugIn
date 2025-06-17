# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox
from qgis.PyQt.QtGui import QIcon, QColor

# Lógica y capas principales
from qgis.core import (
    QgsProject,
    QgsRasterLayer,
    Qgis
)

# Herramientas de mapa y GUI
from qgis.gui import (
    QgsMapToolEmitPoint,
    QgsVertexMarker
)

import os
import math

PLUGIN_NAME = "PhotoMetrix"

class MeasurementMapTool(QgsMapToolEmitPoint):
    def __init__(self, iface):
        super().__init__(iface.mapCanvas())
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.state = "CALIBRATE_1"
        self.first_point = None
        self.calibration_pixels = 0.0
        self.markers = []

    def activate(self):
        super().activate()
        self.iface.messageBar().pushMessage(
            "Paso 1: Calibración",
            "Haga clic en el primer punto de su referencia de 1 metro.",
            level=Qgis.Info,
            duration=0
        )
        self.canvas.setCursor(Qgis.Cursor.Cross)

    def deactivate(self):
        super().deactivate()
        self.iface.messageBar().clearWidgets()
        self._clear_markers()

    def canvasClicked(self, point, button):
        if self.state == "CALIBRATE_1":
            self.first_point = point
            self._add_marker(point, QColor("blue"))
            self.state = "CALIBRATE_2"
            self.iface.messageBar().pushMessage(
                "Paso 1: Calibración",
                "Haga clic en el segundo punto de su referencia de 1 metro.",
                level=Qgis.Info,
                duration=0
            )
        elif self.state == "CALIBRATE_2":
            second_point = point
            self._add_marker(second_point, QColor("blue"))
            dx = self.first_point.x() - second_point.x()
            dy = self.first_point.y() - second_point.y()
            self.calibration_pixels = math.sqrt(dx**2 + dy**2)
            if self.calibration_pixels == 0:
                self.iface.messageBar().pushMessage(
                    "Error", "La distancia de calibración no puede ser cero. Inténtelo de nuevo.",
                    level=Qgis.Critical, duration=5
                )
                self.reset_calibration()
                return
            self.iface.messageBar().pushMessage(
                "Calibración Completa",
                f"Referencia de 1m establecida a {self.calibration_pixels:.2f} píxeles. Ahora puede medir.",
                level=Qgis.Success, duration=5
            )
            self.state = "MEASURE_1"
            self.first_point = None
            self._clear_markers_after_delay(1000)
            self.iface.messageBar().pushMessage(
                "Paso 2: Medición",
                "Haga clic en el primer punto de la distancia que desea medir.",
                level=Qgis.Info, duration=0
            )
        elif self.state == "MEASURE_1":
            self._clear_markers()
            self.first_point = point
            self._add_marker(point, QColor("red"))
            self.state = "MEASURE_2"
            self.iface.messageBar().pushMessage(
                "Paso 2: Medición",
                "Haga clic en el segundo punto de la distancia.",
                level=Qgis.Info, duration=0
            )
        elif self.state == "MEASURE_2":
            second_point = point
            self._add_marker(second_point, QColor("red"))
            dx = self.first_point.x() - second_point.x()
            dy = self.first_point.y() - second_point.y()
            measure_pixels = math.sqrt(dx**2 + dy**2)
            scale_m_per_pixel = 1.0 / self.calibration_pixels
            real_distance_m = measure_pixels * scale_m_per_pixel
            QMessageBox.information(
                self.iface.mainWindow(),
                "Resultado de la Medición",
                f"La distancia medida es: {real_distance_m:.3f} metros."
            )
            self.state = "MEASURE_1"
            self.first_point = None
            self.iface.messageBar().pushMessage(
                "Paso 2: Medición",
                "Medición completada. Haga clic en el primer punto para una nueva medición.",
                level=Qgis.Info, duration=0
            )

    def reset_calibration(self):
        self._clear_markers()
        self.state = "CALIBRATE_1"
        self.first_point = None
        self.calibration_pixels = 0.0
        self.activate()

    def _add_marker(self, point, color):
        marker = QgsVertexMarker(self.canvas)
        marker.setCenter(point)
        marker.setColor(color)
        marker.setIconType(QgsVertexMarker.ICON_CROSS)
        marker.setIconSize(12)
        marker.setPenWidth(3)
        self.markers.append(marker)

    def _clear_markers(self):
        for marker in self.markers:
            self.canvas.scene().removeItem(marker)
        self.markers = []

    def _clear_markers_after_delay(self, ms):
        from qgis.PyQt.QtCore import QTimer
        QTimer.singleShot(ms, self._clear_markers)

class PhotoMetrix:
    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.map_tool = None
        self.plugin_dir = os.path.dirname(__file__)

    def initGui(self):
        icon_path = os.path.join(self.plugin_dir, "icon.png")
        self.action = QAction(QIcon(icon_path), "Medidor de imágenes", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(f"&{PLUGIN_NAME}", self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginToMenu(f"&{PLUGIN_NAME}", self.action)
        if self.map_tool:
            self.iface.mapCanvas().unsetMapTool(self.map_tool)

    def run(self):
        image_path, _ = QFileDialog.getOpenFileName(
            self.iface.mainWindow(),
            "Seleccione una imagen para medir",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
        )
        if not image_path:
            return
        layer_name = os.path.basename(image_path)
        raster_layer = QgsRasterLayer(image_path, layer_name)
        if not raster_layer.isValid():
            QMessageBox.critical(None, "Error", "No se pudo cargar el archivo de imagen como capa.")
            return
        QgsProject.instance().addMapLayer(raster_layer)
        self.iface.mapCanvas().setExtent(raster_layer.extent())
        self.iface.mapCanvas().refresh()
        instructions = (
            "Bienvenido al Medidor de Imágenes.\n\n"
            "El proceso consta de dos pasos:\n\n"
            "1. CALIBRACIÓN: Deberá hacer clic en dos puntos de la imagen que representen una distancia conocida de 1 metro.\n\n"
            "2. MEDICIÓN: Una vez calibrado, podrá hacer clic en dos puntos cualesquiera para medir la distancia entre ellos en metros.\n\n"
            "Siga las instrucciones que aparecerán en la barra de mensajes amarilla en la parte superior del mapa.\n\n"
            "Para salir de la herramienta, seleccione cualquier otra herramienta del mapa (ej. Mover Mapa)."
        )
        QMessageBox.information(self.iface.mainWindow(), "Instrucciones de Uso", instructions)
        self.map_tool = MeasurementMapTool(self.iface)
        self.iface.mapCanvas().setMapTool(self.map_tool) 