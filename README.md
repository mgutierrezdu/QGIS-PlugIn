# QGIS Plugins: Image Geolocator & Plugin Generator

Este repositorio contiene dos complementos desarrollados para QGIS, orientados a facilitar el trabajo con imágenes georreferenciadas y la creación de nuevos plugins.

---

## 🧩 Plugin 1: Image Geolocator

Este plugin permite importar imágenes con coordenadas GPS embebidas en sus metadatos EXIF y mostrarlas como puntos georreferenciados en el lienzo de QGIS.

### 🔧 Funciones principales
- Selección de carpeta con imágenes `.jpg`.
- Extracción de coordenadas desde metadatos EXIF GPS.
- Creación de capa de puntos en QGIS con nombre de imagen como atributo.

### 📦 Instalación
1. Copiar la carpeta `image_geolocator` en el directorio de plugins de QGIS:
   - **Windows**: `C:\Users\<usuario>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
2. Asegúrate de que `resources.py` esté presente (ya incluido).
3. Activa el plugin desde **Complementos > Administrar e instalar complementos**.

---

## 🧩 Plugin 2: Plugin Generator

Este plugin permite crear automáticamente la estructura base de un nuevo plugin de QGIS con carpetas, archivos y plantillas listas para desarrollar.

### 🔧 Funciones principales
- Entrada de nombre visible y autores del nuevo plugin.
- El nombre visible puede contener espacios y caracteres especiales, pero el generador creará automáticamente nombres de clase y archivos válidos para Python (sin espacios ni caracteres especiales).
- Creación automática de:
  - `metadata.txt`, `main.py`, `dialog.py`, `gui.ui`
  - carpetas estándar: `forms/`, `icons/`, `resources/`, `i18n/`
- Permite cargar archivos personalizados (`main.py`, `dialog.py`, `.ui`).
- Si deseas widgets/interfaz, debes cargar tu propio `main.py`, `dialog.py` y `.ui` personalizados. El generador no modifica el código del usuario.
- El template base de `main.py` es flexible y sirve para plugins de lógica, de mapa o de interfaz.

### ⚡️ Bloque de imports recomendado

El template base de `main.py` incluye imports de `qgis.core` y `qgis.gui` para máxima compatibilidad. **Elimina los que no uses para mantener tu plugin limpio.**

```python
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox
from qgis.PyQt.QtGui import QIcon, QColor

# Lógica y capas principales
from qgis.core import (
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsField,
    QgsFields,
    Qgis
)

# Herramientas de mapa y GUI (descomenta o elimina según tu plugin)
from qgis.gui import (
    QgsMapToolEmitPoint,
    QgsVertexMarker,
    QgsMapTool,
    QgsRubberBand,
    QgsMapCanvas
)

import os
import math
```

---

## 👥 Autores

- **Image Geolocator**: Miguel Ángel Gutiérrez Duque & Jerónimo Vargas Gómez
  ✉️ mgutierrezdu@unal.edu.co, jervargasgo@unal.edu.co

- **Plugin Generator**: Miguel Ángel Gutiérrez Duque & Jerónimo Vargas Gómez  
  ✉️ mgutierrezdu@unal.edu.co, jervargasgo@unal.edu.co

---

## 📌 Requisitos

- QGIS 3.16 o superior
- Python 3.x
- PyQt5, exifread

---

## 🗂 Estructura del Repositorio

```
QGIS-PlugIn/
├── image_geolocator/
│   └── [archivos del plugin 1]
├── plugin_generator/
│   └── [archivos del plugin 2]
```

---

## 📦 Instalación desde archivo ZIP

Puedes instalar cualquiera de los plugins directamente desde QGIS usando los archivos `.zip` generados:

1. Abre QGIS.
2. Ve a **Complementos > Administrar e instalar complementos**.
3. Selecciona la pestaña **"Instalar desde archivo ZIP"**.
4. Elige el archivo correspondiente (`image_geolocator.zip` o `plugin_generator.zip`).
5. Haz clic en **"Instalar complemento"**.
6. Activa el plugin desde la pestaña "Instalado" si no se activa automáticamente.

Con esto evitarás tener que mover carpetas manualmente o compilar recursos.

