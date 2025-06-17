# -*- coding: utf-8 -*-
"""
Unified Geolocator Plugin - Main Plugin Class
Combines image geolocation and distance calculation functionality
"""

from qgis.PyQt.QtWidgets import QAction, QMessageBox
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsProject
import os

from .unified_dialog import UnifiedGeolocatorDialog

class UnifiedGeolocatorPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.dialog = None

    def initGui(self):
        """Initialize the plugin GUI"""
        icon_path = os.path.join(os.path.dirname(__file__), "icons", "icon.png")
        self.action = QAction(
            QIcon(icon_path) if os.path.exists(icon_path) else QIcon(),
            "Unified Geolocator",
            self.iface.mainWindow()
        )
        self.action.setObjectName('UnifiedGeolocatorAction')
        self.action.setWhatsThis("Geolocalizar imágenes y calcular distancias")
        self.action.setStatusTip("Abrir interfaz unificada de geolocalización")
        self.action.triggered.connect(self.run)
        
        # Add to toolbar and menu
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Unified Geolocator", self.action)

    def unload(self):
        """Unload the plugin"""
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginMenu("&Unified Geolocator", self.action)

    def run(self):
        """Run the plugin"""
        try:
            if not self.dialog:
                self.dialog = UnifiedGeolocatorDialog(self.iface)
            self.dialog.show()
            self.dialog.raise_()
            self.dialog.activateWindow()
        except Exception as e:
            QMessageBox.critical(
                self.iface.mainWindow(),
                "Error",
                f"Error al abrir la interfaz unificada: {str(e)}"
            ) 