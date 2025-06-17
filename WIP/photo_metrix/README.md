# PhotoMetrix: Medidor de Distancias en Imágenes para QGIS

PhotoMetrix es un plugin autocontenido para QGIS que permite medir distancias reales sobre imágenes rasterizadas, calibrando manualmente una referencia de 1 metro en la imagen. No requiere archivos de interfaz ni dependencias adicionales: toda la lógica está en un único archivo `main.py`.

---

## 🚀 ¿Qué hace este plugin?
- Permite al usuario seleccionar una imagen y cargarla como capa raster en QGIS.
- Solicita al usuario que calibre la escala haciendo clic en dos puntos que representen 1 metro en la imagen.
- Permite medir distancias entre cualquier par de puntos en la imagen, mostrando el resultado en metros.
- Utiliza la barra de mensajes de QGIS y ventanas emergentes para guiar al usuario paso a paso.
- No utiliza diálogos persistentes ni archivos `.ui`.

---

## 🧭 Flujo de trabajo
1. Haz clic en el botón del plugin en la barra de herramientas de QGIS.
2. Selecciona una imagen desde tu disco.
3. La imagen se carga como capa raster y se ajusta la vista.
4. Aparecen instrucciones en pantalla:
   - Calibra la escala haciendo clic en dos puntos que representen 1 metro real.
   - Luego, haz clic en dos puntos para medir la distancia real entre ellos.
5. El resultado de la medición se muestra en una ventana emergente.
6. Puedes repetir el proceso de medición sin recalibrar, o recalibrar si lo deseas.

---

## 🛠 Instalación
1. Copia la carpeta `photo_metrix` (con el archivo `main.py`) en el directorio de plugins de QGIS:
   - **Windows**: `C:\Users\<usuario>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
2. (Opcional) Agrega un `icon.png` para personalizar el botón del plugin.
3. Activa el plugin desde **Complementos > Administrar e instalar complementos**.

---

## 📋 Requisitos
- QGIS 3.16 o superior
- Python 3.x
- PyQt5

---

## 💡 Notas
- El plugin es autocontenido: solo requiere el archivo `main.py`.
- No utiliza archivos de interfaz (`dialog.py`, `.ui`).
- El código es fácilmente modificable para adaptarse a otros flujos de medición o calibración.

---

## 👥 Autor
- Basado en ideas y código de la comunidad QGIS y adaptado por el equipo de desarrollo del repositorio. 