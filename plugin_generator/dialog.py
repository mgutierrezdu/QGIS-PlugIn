from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
import os

class PluginGeneratorDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Cambiar para hacer referencia al archivo gui.ui correcto
        ui_file = os.path.join(os.path.dirname(__file__), "forms", "gui.ui")
        uic.loadUi(ui_file, self)
