# Plugin QGIS: Plugin Generator

Este plugin permite generar automáticamente la estructura básica de un nuevo plugin para QGIS.

## 📦 Estructura del plugin

```
plugin_generator/
├── __init__.py
├── main.py
├── metadata.txt
├── resources.qrc
├── forms/
│   └── gui.ui
├── icons/
│   └── icon.png
├── template_files/
│   ├── metadata.txt
│   ├── plugin_base.py
│   └── plugin_gui.ui
├── i18n/
├── resources/
└── resources.py  ← generado con pyrcc5
```

## ⚙️ Instalación

### 1. Compilar recursos (En caso de no ver el archivo resources.py)

```bash
pyrcc5 resources.qrc -o resources.py
```

### 2. Copiar el plugin a QGIS

#### En Linux:
```bash
cp -r plugin_generator ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/
```

#### En Windows:
```
C:\Users\<TU_USUARIO>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\
```

### 3. Activar el plugin

1. Abrir QGIS.
2. Ir a **Complementos > Administrar e instalar complementos**.
3. Buscar **Plugin Generator** y activarlo.

## 🚀 Uso

1. Clic en el botón del plugin.
2. Selecciona la carpeta donde se creará el nuevo plugin.
3. Ingresa el nombre del nuevo plugin.
4. Se generará una carpeta con la estructura básica del plugin en el destino seleccionado.

## ✍️ Personalización

- Los archivos `metadata.txt`, `plugin_base.py` y `plugin_gui.ui` sirven como plantilla base y pueden personalizarse.
- El campo `plugin_name` será reemplazado automáticamente por el nombre del nuevo plugin.

---

Autores:  
- Miguel Ángel Gutiérrez Duque (mgutierrezdu@unal.edu.co)  
- Jerónimo Vargas Gómez (jervargasgo@unal.edu.co)


---

## 📦 Instalación alternativa (archivo ZIP)

Si descargaste el archivo `plugin_generator.zip`, puedes instalarlo directamente:

1. Abre QGIS.
2. Ve a **Complementos > Administrar e instalar complementos**.
3. Usa la pestaña **"Instalar desde archivo ZIP"**.
4. Selecciona `plugin_generator.zip`.
5. Haz clic en **"Instalar complemento"** y actívalo.

No es necesario compilar `resources.qrc` ni copiar carpetas manualmente.
