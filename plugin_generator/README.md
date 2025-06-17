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

- Los archivos `metadata.txt`, `main.py`, `dialog.py` y `gui.ui` sirven como plantilla base y pueden personalizarse.
- El campo `plugin_name` será reemplazado automáticamente por el nombre del nuevo plugin.

### ⚠️ Sobre la interfaz y widgets

- **Por defecto, el plugin generado NO tiene interfaz ni widgets.**
- **Si deseas que tu plugin tenga widgets/interfaz gráfica, debes cargar tu propio `main.py`, `dialog.py` y `.ui` personalizados.**
- El generador no modifica ni valida el código del usuario. Si tu código accede a widgets, asegúrate de que existan en tu `.ui` y `dialog.py`.
- Si no cargas archivos personalizados, el plugin generado será mínimo y robusto, sin referencias a widgets.

#### Ejemplo: Acceso seguro a widgets en tu main.py

```python
# En tu main.py personalizado, accede a widgets así:
if hasattr(self.dlg, 'browseButton'):
    self.dlg.browseButton.clicked.connect(self.browse_folder)
if hasattr(self.dlg, 'runButton'):
    self.dlg.runButton.clicked.connect(self.run_process)
if hasattr(self.dlg, 'statusLabel'):
    self.dlg.statusLabel.setText("")
```

Esto evita errores si el widget no existe (por ejemplo, si generas un plugin sin interfaz).

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
