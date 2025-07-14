from .main import PluginGenerator  # Asegúrate de usar la clase correcta del plugin generado

def classFactory(iface):
    """
    Esta función se llama cuando QGIS carga el plugin.
    Se debe asegurar de retornar la clase que gestiona la interfaz del plugin.
    """
    return PluginGenerator(iface)  # Asegúrate de que la clase que retorna sea la clase principal del plugin
