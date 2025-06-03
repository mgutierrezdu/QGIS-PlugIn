# -*- coding: utf-8 -*-
import os
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox, QInputDialog
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QDate
from shutil import copyfile

class PluginGenerator:
    def __init__(self, iface):
        self.iface = iface
        self.action = None

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(__file__), "icons", "icon.png")
        self.action = QAction(QIcon(icon_path), "Generar nuevo plugin QGIS", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Plugin Generator", self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginMenu("&Plugin Generator", self.action)

    def run(self):
        base_dir = QFileDialog.getExistingDirectory(None, "Selecciona la carpeta donde se creará el nuevo plugin")
        if not base_dir:
            return

        name, ok = QInputDialog.getText(None, "Nombre del Plugin", "Introduce el nombre del nuevo plugin:")
        if not ok or not name:
            return

        plugin_dir = os.path.join(base_dir, name)
        if os.path.exists(plugin_dir):
            QMessageBox.warning(None, "Advertencia", "La carpeta del plugin ya existe.")
            return

        os.makedirs(plugin_dir)
        for folder in ["forms", "icons", "resources", "i18n"]:
            os.makedirs(os.path.join(plugin_dir, folder), exist_ok=True)

        template_path = os.path.join(os.path.dirname(__file__), "template_files")

        for filename in os.listdir(template_path):
            src = os.path.join(template_path, filename)
            dst = os.path.join(plugin_dir, filename)
            copyfile(src, dst)

        # Personaliza metadata
        metadata_path = os.path.join(plugin_dir, "metadata.txt")
        with open(metadata_path, "r+") as f:
            content = f.read()
            content = content.replace("plugin_name", name)
            content = content.replace("YYYY-MM-DD", QDate.currentDate().toString("yyyy-MM-dd"))
            f.seek(0)
            f.write(content)
            f.truncate()

        msg = f"Plugin '{name}' creado exitosamente en:\n{plugin_dir}"
        QMessageBox.information(None, "Plugin creado", msg)
