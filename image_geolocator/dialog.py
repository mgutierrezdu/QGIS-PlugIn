# -*- coding: utf-8 -*-
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
import os

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "forms", "gui.ui")
)

class ImageGeolocatorDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(ImageGeolocatorDialog, self).__init__(parent)
        self.setupUi(self)
