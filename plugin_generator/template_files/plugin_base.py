# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import QAction, QDialog
from qgis.PyQt.QtGui import QIcon
import os

class plugin_name:
    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.dialog = None

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        self.action = QAction(QIcon(icon_path), "plugin_name", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&plugin_name", self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginMenu("&plugin_name", self.action)

    def run(self):
        if not self.dialog:
            self.dialog = QDialog()
        self.dialog.show()
