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
- Entrada de nombre del nuevo plugin.
- Creación automática de:
  - `metadata.txt`, `plugin_base.py`, `plugin_gui.ui`
  - carpetas estándar: `forms/`, `icons/`, `resources/`, `i18n/`

### 📦 Instalación
1. Copiar la carpeta `plugin_generator` al directorio de plugins de QGIS.
2. Ejecutar QGIS y activar el plugin.
3. Usar el botón del plugin para crear nuevos proyectos de complemento.

---

## 👥 Autores

- **Image Geolocator**: Miguel Ángel Gutiérrez Duque & Jerónimo Vargas Gómez  
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

