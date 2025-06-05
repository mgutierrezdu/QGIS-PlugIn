from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox
from qgis.PyQt.QtGui import QIcon

class PluginGenerator:
    def __init__(self, iface):
        self.iface = iface
        self.action = None

    def initGui(self):
        icon_path = "icons/icon.png"  # Asegúrate de que el ícono esté en la carpeta correcta
        self.action = QAction(QIcon(icon_path), "Generar nuevo plugin", self.iface.mainWindow())
        self.iface.addToolBarIcon(self.action)
        self.action.triggered.connect(self.run)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        # Lógica del plugin aquí
        QMessageBox.information(None, "Información", "Plugin Generado")

def classFactory(iface):
    return PluginGenerator(iface)
