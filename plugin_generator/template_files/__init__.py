from .main import {{ plugin_class_name }}

def classFactory(iface):
    return {{ plugin_class_name }}(iface)
