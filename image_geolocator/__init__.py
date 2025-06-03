# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ImageGeolocator
                                 A QGIS Plugin
 Geolocaliza imágenes usando coordenadas GPS en los metadatos EXIF
                              -------------------
        begin                : 2025-05-29
        author               : Miguel Ángel Gutiérrez Duque & Jerónimo Vargas Gómez
        email                : mgutierrezdu@unal.edu.co, jervargasgo@unal.edu.co
 ***************************************************************************/
"""

def classFactory(iface):
    from .main import ImageGeolocator
    return ImageGeolocator(iface)
