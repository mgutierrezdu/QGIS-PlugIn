from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
import os

class PluginGeneratorDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Cargar un archivo .ui si está disponible, de lo contrario, cargar la interfaz predeterminada
        ui_file = os.path.join(os.path.dirname(__file__), "forms", "gui.ui")
        uic.loadUi(ui_file, self)

        # Definir los botones y conexiones
        self.browsePythonButton.clicked.connect(self.load_python_file)
        self.browseUIButton.clicked.connect(self.load_ui_file)
        self.browseIconButton.clicked.connect(self.load_icon_file)
        self.generateButton.clicked.connect(self.generate_plugin)

    def load_python_file(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Selecciona un archivo .py", "", "Python Files (*.py)")
        if file_path:
            with open(file_path, "r") as f:
                python_code = f.read()
            self.pythonCodeTextEdit.setPlainText(python_code)

    def load_ui_file(self):
        ui_file, _ = QFileDialog.getOpenFileName(None, "Selecciona un archivo .ui", "", "UI Files (*.ui)")
        if ui_file:
            ui_file_name = os.path.basename(ui_file)
            if ui_file_name != "gui.ui":
                QMessageBox.warning(None, "Error", "El archivo .ui debe llamarse gui.ui")
            else:
                self.uiFileLineEdit.setText(ui_file)

    def load_icon_file(self):
        icon_file, _ = QFileDialog.getOpenFileName(None, "Selecciona un ícono", "", "Icon Files (*.png *.jpg *.svg)")
        if icon_file:
            self.iconFileLineEdit.setText(icon_file)

    def generate_plugin(self):
        # Lógica de generación del plugin
        pass
