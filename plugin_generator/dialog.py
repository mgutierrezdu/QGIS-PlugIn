from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QFileDialog
import os

class PluginGeneratorDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Cambiar para hacer referencia al archivo gui.ui correcto
        ui_file = os.path.join(os.path.dirname(__file__), "forms", "gui.ui")
        uic.loadUi(ui_file, self)

        self.dialogPythonCode = None
        self.browseDialogButton.clicked.connect(self.load_dialog_python_file)

    def load_dialog_python_file(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Selecciona un archivo dialog.py", "", "Python Files (*.py)")
        if file_path:
            self.dialogPythonFileLineEdit.setText(file_path)
            with open(file_path, "r", encoding="utf-8") as f:
                self.dialogPythonCode = f.read()

    @property
    def plugin_name(self):
        return self.pluginNameLineEdit.text().strip() or "NuevoPlugin"

    @property
    def plugin_authors(self):
        return self.pluginAuthorsLineEdit.text().strip() or "Autor Desconocido"
