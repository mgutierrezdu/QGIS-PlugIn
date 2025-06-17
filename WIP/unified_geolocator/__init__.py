# -*- coding: utf-8 -*-
"""
Unified Geolocator Plugin for QGIS
Combines image geolocation and distance calculation in one interface
"""

def classFactory(iface):
    from .main import UnifiedGeolocatorPlugin
    return UnifiedGeolocatorPlugin(iface) 