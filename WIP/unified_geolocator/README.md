# Unified Geolocator Plugin para QGIS

Un plugin unificado que combina funcionalidades de geolocalización de imágenes y análisis de distancias en una interfaz integrada.

## Características

### 🗺️ Geolocalización de Imágenes
- Extracción automática de datos GPS de imágenes (JPG, JPEG, PNG, TIFF)
- Visualización de puntos geolocalizados en el mapa de QGIS
- Soporte para múltiples formatos de imagen
- Manejo de errores para imágenes sin datos GPS

### 📏 Análisis de Distancias
- Cálculo de distancias entre objetos detectados en imágenes
- Múltiples métodos de calibración
- Análisis en lote de múltiples imágenes
- Integración con modelos de IA para detección de objetos

### 🎯 Interfaz Unificada
- Panel de control intuitivo con pestañas organizadas
- Vista de resultados en tabla
- Vista de mapa integrada
- Estadísticas detalladas del procesamiento

### 📊 Exportación de Datos
- Exportación a formato CSV
- Exportación a formato GeoJSON
- Creación automática de capas vectoriales en QGIS

## Instalación

1. Descarga el plugin desde el repositorio
2. Extrae el archivo en la carpeta de plugins de QGIS:
   - Windows: `C:\Users\[Usuario]\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - Linux: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
   - macOS: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`
3. Activa el plugin en QGIS: Plugins → Manage and Install Plugins → Installed

## Uso

### Procesamiento Básico
1. Abre el plugin desde la barra de herramientas
2. Selecciona una carpeta con imágenes
3. Marca las opciones de procesamiento deseadas
4. Haz clic en "Procesar Imágenes"
5. Revisa los resultados en las diferentes pestañas

### Opciones de Procesamiento
- **Geolocalizar imágenes**: Extrae datos GPS y crea puntos en el mapa
- **Analizar imágenes**: Realiza análisis de distancias
- **Agregar mapa base**: Carga OpenStreetMap como mapa base
- **Crear capa vectorial**: Genera una capa en QGIS con los resultados

### Exportación
- **CSV**: Exporta resultados en formato de tabla
- **GeoJSON**: Exporta datos geoespaciales para uso en otras aplicaciones

## Requisitos

- QGIS 3.0 o superior
- Python 3.6+
- Bibliotecas adicionales:
  - `exifread` (para extracción de metadatos GPS)
  - `Pillow` (para procesamiento de imágenes)
  - `ultralytics` (para análisis de distancias - opcional)

## Instalación de Dependencias

```bash
pip install exifread Pillow
# Para análisis avanzado de distancias:
pip install ultralytics opencv-python
```

## Estructura del Proyecto

```
unified_geolocator/
├── __init__.py              # Punto de entrada del plugin
├── main.py                  # Clase principal del plugin
├── unified_dialog.py        # Interfaz unificada
├── metadata.txt             # Metadatos del plugin
├── README.md               # Este archivo
└── icons/
    └── icon.png            # Icono del plugin
```

## Funcionalidades Avanzadas

### Análisis de Distancias
El plugin incluye múltiples métodos para calcular distancias:

1. **Calibración GPS**: Usa datos de altitud y parámetros de cámara
2. **Distancia de referencia**: Calibración manual con objetos conocidos
3. **Estimación por edificios**: Aproximación basada en alturas típicas

### Procesamiento en Lote
- Procesa múltiples imágenes simultáneamente
- Barra de progreso en tiempo real
- Manejo de errores individual por imagen

## Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Soporte

Para reportar bugs o solicitar nuevas funcionalidades, por favor usa la sección de Issues del repositorio.

## Changelog

### v1.0.0
- Versión inicial
- Geolocalización básica de imágenes
- Interfaz unificada
- Exportación a CSV y GeoJSON
- Integración con QGIS 