
# R2 Cameras - Proyecto de Modelos 3D y Cámaras

Este proyecto es una extensión del anterior rasterizador, pero con un enfoque en diferentes ángulos de cámara para visualizar los modelos 3D. Se exploran varias perspectivas como la vista superior, inferior, y ángulos inclinados, entre otros. El proyecto está desarrollado en Python y utiliza módulos personalizados para la manipulación de las cámaras y operaciones gráficas.

## Contenido del Proyecto

El proyecto contiene los siguientes archivos:

### Archivos de Código:
- **camera.py**: Contiene la lógica para la manipulación de cámaras y la configuración de diferentes ángulos de visualización del modelo 3D.
- **gl.py**: La lógica principal para el rasterizador, como la inicialización del frame buffer y la generación de imágenes BMP desde diferentes ángulos de cámara.
- **mathl.py**: Funciones matemáticas para la manipulación de vectores y matrices 3D.
- **model.py**: Gestión de la carga y manipulación de modelos 3D.
- **obj.py**: Utilidades para la carga de archivos `.obj` y su interpretación.
- **Rasterizer.py**: Coordina el proceso de rasterización, incluyendo la integración con las cámaras.
- **shaders.py**: Contiene las funciones para aplicar efectos de sombreado a los modelos renderizados.

### Archivos de Imágenes:
- **pez.obj**: El modelo 3D utilizado en el proyecto.
- **pez.bmp / pez.jpg**: Representaciones del modelo renderizado en diferentes formatos.
- **bottom.bmp**: Imagen renderizada desde la vista inferior.
- **dutch.bmp**: Imagen renderizada desde un ángulo inclinado (vista Dutch).
- **medium.bmp**: Imagen renderizada desde una vista media.
- **top.bmp**: Imagen renderizada desde la vista superior.

### Otros Archivos:
- **README.md**: Este archivo de documentación.

## Cómo Ejecutar el Proyecto

1. Instala Python en tu máquina si no lo tienes instalado.
2. Clona el repositorio y navega hasta la carpeta del proyecto.
3. Ejecuta `Rasterizer.py` para cargar el modelo y generar las imágenes desde diferentes ángulos de cámara.
4. Las imágenes de salida se guardarán en formato BMP en la carpeta raíz del proyecto.

## Dependencias

Este proyecto no requiere dependencias externas adicionales más allá de Python.

## Contacto

Gabriel Paz 221087
UNIVERSIDAD DEL VALLE DE GUATEMALA