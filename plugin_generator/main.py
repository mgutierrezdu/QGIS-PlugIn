# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox
from qgis.PyQt.QtGui import QIcon
from qgis.core import (
    QgsProject, QgsPointXY, QgsGeometry, QgsFeature,
    QgsVectorLayer, QgsFields, QgsField, QgsRasterLayer
)
from qgis.PyQt.QtCore import QVariant
import exifread
import os
import shutil
import zipfile

# Importar la clase correcta desde dialog.py
from .dialog import PluginGeneratorDialog

class PluginGenerator:
    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.dialog = None

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(__file__), "icons", "icon.png")
        self.action = QAction(QIcon(icon_path), "Generar nuevo plugin QGIS", self.iface.mainWindow())
        self.action.triggered.connect(self.show_dialog)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Plugin Generator", self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginMenu("&Plugin Generator", self.action)

    def show_dialog(self):
        if not self.dialog:
            self.dialog = PluginGeneratorDialog()
            self.dialog.browsePythonButton.clicked.connect(self.load_python_file)
            self.dialog.browseUIButton.clicked.connect(self.load_ui_file)
            self.dialog.browseIconButton.clicked.connect(self.load_icon_file)
            self.dialog.generateButton.clicked.connect(self.generate_plugin)
        self.dialog.statusLabel.setText("")
        self.dialog.show()
        self.dialog.raise_()
        self.dialog.activateWindow()

    def load_python_file(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Selecciona un archivo .py", "", "Python Files (*.py)")
        if file_path:
            with open(file_path, "r") as f:
                python_code = f.read()
            self.dialog.pythonCodeTextEdit.setPlainText(python_code)

    def load_ui_file(self):
        ui_file, _ = QFileDialog.getOpenFileName(None, "Selecciona un archivo .ui", "", "UI Files (*.ui)")
        if ui_file:
            ui_file_name = os.path.basename(ui_file)
            if ui_file_name != "gui.ui":
                QMessageBox.warning(None, "Error", "El archivo .ui debe llamarse gui.ui")
            else:
                self.dialog.uiFileLineEdit.setText(ui_file)

    def load_icon_file(self):
        icon_file, _ = QFileDialog.getOpenFileName(None, "Selecciona un ícono", "", "Icon Files (*.png *.jpg *.svg)")
        if icon_file:
            self.dialog.iconFileLineEdit.setText(icon_file)

    def generate_plugin(self):
        # Obtener carpeta de destino
        folder = QFileDialog.getExistingDirectory(None, "Selecciona la carpeta donde se creará el plugin")
        if not folder:
            return

        # Crear la carpeta del nuevo plugin
        plugin_name = "NuevoPlugin"  # O algún nombre proporcionado por el usuario
        plugin_dir = os.path.join(folder, plugin_name)
        if os.path.exists(plugin_dir):
            QMessageBox.warning(None, "Advertencia", "La carpeta del plugin ya existe.")
            return

        os.makedirs(plugin_dir)
        os.makedirs(os.path.join(plugin_dir, "forms"))
        os.makedirs(os.path.join(plugin_dir, "icons"))
        os.makedirs(os.path.join(plugin_dir, "resources"))
        os.makedirs(os.path.join(plugin_dir, "i18n"))

        # Copiar los archivos base del plugin
        template_path = os.path.join(os.path.dirname(__file__), "template_files")
        for filename in os.listdir(template_path):
            src = os.path.join(template_path, filename)
            dst = os.path.join(plugin_dir, filename)
            shutil.copy(src, dst)

        # Guardar el código Python ingresado o cargado
        python_code = self.dialog.pythonCodeTextEdit.toPlainText()
        if python_code:
            with open(os.path.join(plugin_dir, "main.py"), "w") as f:
                f.write(python_code)
        else:
            QMessageBox.warning(None, "Advertencia", "No se ingresó ningún código Python.")

        # Si se cargó un archivo .ui, reemplazar la interfaz generica
        ui_file_path = self.dialog.uiFileLineEdit.text()
        if ui_file_path:
            ui_dest = os.path.join(plugin_dir, "forms", "gui.ui")
            shutil.copy(ui_file_path, ui_dest)
        else:
            # Si no se carga un archivo .ui, se usa el predeterminado
            default_ui_path = os.path.join(os.path.dirname(__file__), "template_files", "gui.ui")
            shutil.copy(default_ui_path, os.path.join(plugin_dir, "forms", "gui.ui"))

        # Si se cargó un archivo de ícono, reemplazar el ícono predeterminado
        icon_file_path = self.dialog.iconFileLineEdit.text()
        if icon_file_path:
            shutil.copy(icon_file_path, os.path.join(plugin_dir, "icons", "icon.png"))
        else:
            # Si no se carga un ícono, se usa el ícono predeterminado
            default_icon_path = os.path.join(os.path.dirname(__file__), "icons", "default_icon.png")
            shutil.copy(default_icon_path, os.path.join(plugin_dir, "icons", "icon.png"))

        # Comprimir el plugin en un archivo .zip con la estructura correcta (plugin_name como carpeta principal)
        zip_file = os.path.join(folder, f"{plugin_name}.zip")
        shutil.make_archive(zip_file.replace(".zip", ""), 'zip', folder, plugin_name)

        QMessageBox.information(None, "Éxito", f"Plugin '{plugin_name}' generado exitosamente y guardado como .zip en: {zip_file}")
