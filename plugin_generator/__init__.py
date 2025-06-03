# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PluginGenerator
                                 A QGIS Plugin
 Generador automático de la estructura básica de plugins para QGIS
                              -------------------
        begin                : 2025-06-02
        authors             : Miguel Ángel Gutiérrez Duque & Jerónimo Vargas Gómez
        emails              : mgutierrezdu@unal.edu.co, jervargasgo@unal.edu.co
 ***************************************************************************/
"""

def classFactory(iface):
    from .main import PluginGenerator
    return PluginGenerator(iface)
