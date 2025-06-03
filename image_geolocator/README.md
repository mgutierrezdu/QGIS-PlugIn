# Plugin QGIS: Image Geolocator

Este plugin permite importar imágenes con coordenadas GPS embebidas en sus metadatos EXIF y mostrarlas como puntos georreferenciados en el lienzo de QGIS.

## 📦 Estructura del plugin

```
image_geolocator/
├── __init__.py
├── main.py
├── metadata.txt
├── resources.qrc
├── forms/
│   └── gui.ui
├── icons/
│   └── icon.png
├── i18n/
├── resources/
└── resources.py  ← generado con pyrcc5
```

## ⚙️ Instalación

### 1. Compilar el archivo de recursos (En caso de no ver el archivo resources.py)

Desde una terminal en la carpeta del plugin:

```bash
pyrcc5 resources.qrc -o resources.py
```

### 2. Copiar la carpeta del plugin al directorio de QGIS

#### Linux:
```bash
cp -r image_geolocator ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/
```

#### Windows:
```
C:\Users\<TU_USUARIO>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\
```

### 3. Activar el plugin

1. Abrir QGIS.
2. Ir a **Complementos > Administrar e instalar complementos**.
3. Buscar **Image Geolocator** y activarlo.

## 🚀 Uso

1. Hacer clic en el botón del plugin.
2. Seleccionar una carpeta con imágenes (.jpg) que contengan coordenadas GPS en EXIF.
3. QGIS creará una capa con un punto por cada imagen válida.
4. Cada punto incluirá el nombre del archivo de imagen como atributo.

## ℹ️ Notas

- Las imágenes sin coordenadas GPS serán ignoradas.
- Actualmente el plugin soporta imágenes `.jpg` y `.jpeg`.

---

Autor: Miguel Ángel Gutiérrez Duque  
Email: mgutierrezdu@unal.edu.co  


---

## 📦 Instalación alternativa (archivo ZIP)

Si descargaste el archivo `image_geolocator.zip`, puedes instalarlo fácilmente desde QGIS:

1. Abre QGIS.
2. Ve a **Complementos > Administrar e instalar complementos**.
3. Haz clic en **"Instalar desde archivo ZIP"**.
4. Selecciona `image_geolocator.zip`.
5. Haz clic en **"Instalar complemento"** y actívalo.

Con esto no necesitas copiar carpetas manualmente ni compilar recursos.
