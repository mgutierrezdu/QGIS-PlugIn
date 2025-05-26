# QGIS-PlugIn

**QGIS Plugin: Geolocalizador de Imágenes por Metadatos y Futuro Metaplugin**

Este repositorio contiene el código fuente y la documentación para un proyecto de desarrollo de plugins para QGIS con dos componentes principales:

1.  **Plugin de Geolocalización de Imágenes:**
    *   **Objetivo:** Permitir a los usuarios de QGIS seleccionar imágenes (individualmente o por carpetas) y geolocalizarlas automáticamente en el lienzo del mapa.
    *   **Funcionamiento:** El plugin leerá los metadatos EXIF (específicamente las etiquetas GPS de latitud, longitud y, opcionalmente, altitud) de cada imagen y creará una capa de puntos vectoriales con la ubicación correspondiente.
    *   **Utilidad:** Facilita la incorporación rápida de evidencia fotográfica georreferenciada en proyectos GIS.

2.  **Metaplugin (Visión a Largo Plazo):**
    *   **Objetivo:** Desarrollar una herramienta (un plugin que crea plugins) que simplifique y acelere la creación de nuevos plugins para QGIS.
    *   **Funcionamiento (conceptual):** El metaplugin guiaría al desarrollador a través de la configuración inicial de un nuevo plugin (nombre, descripción, tipo de interfaz, etc.) y generaría la estructura de directorios, archivos base (como `__init__.py`, `metadata.txt`, clase principal del plugin, archivo UI básico) y código repetitivo común.
    *   **Utilidad:** Reducir la curva de aprendizaje y el tiempo de desarrollo inicial para quienes deseen crear sus propias herramientas para QGIS.

**Tecnologías Principales:**
*   Python
*   PyQGIS (API de QGIS para Python)
*   Qt (para interfaces de usuario, a través de PyQt o PySide)
*   Librerías para lectura de EXIF (ej. Pillow, exifread)

**Estado Actual:**
*   En desarrollo: Plugin de Geolocalización de Imágenes.
*   Planificado: Metaplugin.
