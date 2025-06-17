# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox
from qgis.PyQt.QtGui import QIcon, QColor

# Lógica y capas principales
from qgis.core import (
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsField,
    QgsFields,
    Qgis
)

# Herramientas de mapa y GUI (descomenta o elimina según tu plugin)
from qgis.gui import (
    QgsMapToolEmitPoint,
    QgsVertexMarker,
    QgsMapTool,
    QgsRubberBand,
    QgsMapCanvas
)

import os
import math

# Elimina los imports que no uses para mantener tu plugin limpio.

# Si usas interfaz personalizada, descomenta esta línea:
# from .dialog import {{ plugin_class_name }}Dialog

class {{ plugin_class_name }}MapTool(QgsMapToolEmitPoint):
    def __init__(self, iface):
        super().__init__(iface.mapCanvas())
        self.iface = iface
        self.canvas = iface.mapCanvas()

    def canvasClicked(self, point, button):
        # Implementa aquí la lógica de tu herramienta de mapa
        pass

class {{ plugin_class_name }}:
    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.dlg = None
        self.map_tool = None
        self.plugin_dir = os.path.dirname(__file__)

    def initGui(self):
        icon_path = os.path.join(self.plugin_dir, "icons", "icon.png")
        self.action = QAction(QIcon(icon_path), "{{ plugin_name }}", self.iface.mainWindow())
        self.iface.addToolBarIcon(self.action)
        self.action.triggered.connect(self.run)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        if self.map_tool:
            self.iface.mapCanvas().unsetMapTool(self.map_tool)

    def run(self):
        # Si usas interfaz personalizada:
        # if self.dlg is None:
        #     self.dlg = {{ plugin_class_name }}Dialog()
        # self.dlg.show()
        # self.dlg.exec_()
        
        # Si usas herramienta de mapa:
        self.map_tool = {{ plugin_class_name }}MapTool(self.iface)
        self.iface.mapCanvas().setMapTool(self.map_tool)

def classFactory(iface):
    return {{ plugin_class_name }}(iface)
