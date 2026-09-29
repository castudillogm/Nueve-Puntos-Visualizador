# Visualizador 3D de Palés y Cubicaje (Mettler Toledo TLD870)

Herramienta web interactiva en 3D para la visualización, análisis de metrología volumétrica y nubes de puntos de palés generados por sistemas de cubicaje **Mettler Toledo Cargoscan TLD870** (archivos `.jdps` y `.ply`).

---

## 🌟 Características

- **Renderizado 3D Interactivo**: Motor Three.js con aceleración WebGL capaz de visualizar nubes de puntos densas (más de 250.000 puntos) a 60 FPS con controles orbitales (rotar, desplazar, zoom).
- **Lectura en Vivo de Archivos `.jdps`**: Carga dinámica mediante botón de selección o arrastrando y soltando (*Drag & Drop*) cualquier archivo `.jdps` o `.ply`.
- **Caja Delimitadora 3D (*Bounding Box*)**: Visualización en wireframe neón y caras translúcidas de la envolvente volumétrica calculada.
- **Los 9 Puntos Clave del Dimensionador**:
  - **4 Vértices Base**: Esquinas $C_1, C_2, C_3, C_4$ que definen la huella del palé.
  - **5 Puntos de Contacto (*Touching Points*)**: Puntos de contacto tangencial exterior ($T_1 \dots T_5$) con sus correspondientes vectores normales orientados hacia afuera.
- **Filtro Avanzado de Suelo (Corte Z)**:
  - Elimina en tiempo real el plano de suelo y los reflejos de la báscula/suelo mediante selector y control deslizante.
  - Ajustes predefinidos: $Z = 0\text{ mm}$, $Z = 15\text{ mm}$ o visualización completa.
- **Telemetría y Metadatos**:
  - Código / Identificador del palé.
  - Dimensiones oficiales ($L \times W \times H$ en cm).
  - Volumen en litros y peso neto en kg.
  - Orientación y rotación angular.
- **Fotografías de las Cámaras**: Visor integrado de las capturas tomadas por las cámaras del dimensionador en el momento de la medición.
- **100% Client-Side**: No requiere instalación de bases de datos ni servidores backend. Funciona directamente en el navegador.

---

## 🚀 Despliegue en GitHub Pages

Para ver este proyecto online en tu propio dominio de GitHub Pages:

1. Ve a tu repositorio en GitHub: **[Nueve-Puntos-Visualizador](https://github.com/castudillogm/Nueve-Puntos-Visualizador)**
2. Haz clic en **Settings** (Configuración) -> **Pages**.
3. En **Source** (Origen), selecciona:
   - Branch: `main`
   - Folder: `/ (root)`
4. Haz clic en **Save** (Guardar).
5. En unos instantes, la web estará disponible públicamente en:
   👉 **`https://castudillogm.github.io/Nueve-Puntos-Visualizador/`**

---

## 📁 Estructura del Repositorio

- `index.html`: Aplicación web principal lista para servir en la raíz.
- `visualizador_3d.html`: Código fuente del visualizador 3D.
- `generate_viewer.py`: Script generador y procesador de nubes de puntos.
- `puntos_clave.csv`: Exportación tabular con los 9 puntos clave de medición.
- Archivos de muestra:
  - `SBCN26078924_192621.jdps` y `SBCN26078924_192621.ply`
  - `SBCN26078925_192627.jdps` y `SBCN26078925_192627.ply`
  - Fotografías de cámaras de muestra (`image1.jpg`, `image2.jpg`, etc.).
