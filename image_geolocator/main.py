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

from .dialog import ImageGeolocatorDialog

class ImageGeolocator:
    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.layer = None
        self.dialog = None

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(__file__), "icons", "icon.png")
        self.action = QAction(QIcon(icon_path), "Geolocalizar imágenes", self.iface.mainWindow())
        self.action.triggered.connect(self.show_dialog)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Image Geolocator", self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginMenu("&Image Geolocator", self.action)

    def show_dialog(self):
        if not self.dialog:
            self.dialog = ImageGeolocatorDialog()
            self.dialog.browseButton.clicked.connect(self.browse_folder)
            self.dialog.runButton.clicked.connect(self.run_process)
        self.dialog.statusLabel.setText("")
        self.dialog.show()
        self.dialog.raise_()
        self.dialog.activateWindow()

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(None, "Selecciona la carpeta con imágenes")
        if folder:
            self.dialog.folderLineEdit.setText(folder)

    def run_process(self):
        folder = self.dialog.folderLineEdit.text()
        if not folder or not os.path.isdir(folder):
            self.dialog.statusLabel.setText("Por favor, selecciona una carpeta válida.")
            return

        self.dialog.statusLabel.setText("Procesando imágenes, por favor espera...")
        self.add_osm_basemap()
        self.create_layer()
        self.process_images(folder)
        self.dialog.statusLabel.setText("¡Proceso completado!")
        
    def create_layer(self):
        self.layer = QgsVectorLayer("Point?crs=EPSG:4326", "Imágenes geolocalizadas", "memory")
        pr = self.layer.dataProvider()
        pr.addAttributes([QgsField("imagen", QVariant.String)])
        self.layer.updateFields()
        QgsProject.instance().addMapLayer(self.layer)

    def process_images(self, folder):
        pr = self.layer.dataProvider()
        for filename in os.listdir(folder):
            if filename.lower().endswith(('.jpg', '.jpeg')):
                path = os.path.join(folder, filename)
                with open(path, 'rb') as f:
                    tags = exifread.process_file(f, stop_tag='GPS GPSLongitude')
                    if "GPS GPSLatitude" in tags and "GPS GPSLongitude" in tags:
                        lat = self._get_decimal_from_dms(tags["GPS GPSLatitude"].values, tags["GPS GPSLatitudeRef"].values)
                        lon = self._get_decimal_from_dms(tags["GPS GPSLongitude"].values, tags["GPS GPSLongitudeRef"].values)
                        feat = QgsFeature(self.layer.fields())
                        feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(lon, lat)))
                        feat.setAttribute("imagen", filename)
                        pr.addFeature(feat)
        self.layer.updateExtents()
        self.layer.triggerRepaint()

    def _get_decimal_from_dms(self, dms, ref):
        degrees = float(dms[0].num) / float(dms[0].den)
        minutes = float(dms[1].num) / float(dms[1].den)
        seconds = float(dms[2].num) / float(dms[2].den)
        decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
        if ref in ['S', 'W']:
            decimal = -decimal
        return decimal

    def add_osm_basemap(self):
        url = "type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png"
        layer = QgsRasterLayer(url, "OpenStreetMap", "wms")
        if layer.isValid():
            QgsProject.instance().addMapLayer(layer, False)
            QgsProject.instance().layerTreeRoot().insertLayer(0, layer)
        else:
            QMessageBox.warning(None, "Error", "No se pudo cargar el mapa base.")
