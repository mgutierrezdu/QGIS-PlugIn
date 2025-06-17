from qgis.PyQt.QtWidgets import QAction, QMessageBox
from qgis.PyQt.QtGui import QIcon
from .dialog import {{ plugin_class_name }}Dialog
import os

# Si deseas widgets/interfaz, debes cargar tu propio main.py, dialog.py y .ui personalizados.
class {{ plugin_class_name }}:
    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.dlg = None

    def initGui(self):
        icon_path = "icons/icon.png"
        self.action = QAction(QIcon(icon_path), "Generar nuevo plugin", self.iface.mainWindow())
        self.iface.addToolBarIcon(self.action)
        self.action.triggered.connect(self.run)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        if self.dlg is None:
            self.dlg = {{ plugin_class_name }}Dialog()
        self.dlg.show()
        self.dlg.exec_()

    # Aquí puedes agregar tu lógica personalizada

def classFactory(iface):
    return {{ plugin_class_name }}(iface)
