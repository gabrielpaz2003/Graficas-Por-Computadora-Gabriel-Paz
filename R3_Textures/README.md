
# R3 Textures - Proyecto de Modelos 3D con Texturas

Este proyecto extiende el rasterizador anterior, añadiendo soporte para el mapeo de texturas en los modelos 3D. Permite cargar y aplicar texturas sobre las superficies de los modelos renderizados. El proyecto está desarrollado en Python y utiliza módulos personalizados para la carga, manipulación y aplicación de texturas.

## Contenido del Proyecto

El proyecto contiene los siguientes archivos:

### Archivos de Código:
- **camera.py**: Controla los ángulos de la cámara y la perspectiva utilizada para visualizar el modelo 3D.
- **gl.py**: Contiene las operaciones de rasterización y el procesamiento general para generar imágenes BMP, con soporte para texturas.
- **mathl.py**: Incluye funciones matemáticas que manejan las operaciones de vectores y matrices necesarias para el renderizado.
- **model.py**: Se encarga de gestionar los modelos 3D y sus transformaciones.
- **obj.py**: Utilidades para cargar archivos `.obj` y convertirlos en datos procesables.
- **Rasterizer.py**: Coordina el proceso de renderizado y la aplicación de texturas sobre los modelos.
- **shaders.py**: Funciones de sombreado para mejorar el aspecto visual de los modelos.
- **texture.py**: Maneja la carga y aplicación de texturas sobre las superficies de los modelos.

### Archivos de Imágenes y Modelos:
- **barril.obj**: El modelo 3D utilizado para este proyecto.
- **barril.bmp**: Imagen renderizada con texturas aplicadas sobre el modelo.
- **output.bmp**: Imagen de salida generada por el rasterizador con texturas.

### Otros Archivos:
- **README.md**: Este archivo de documentación.

## Cómo Ejecutar el Proyecto

1. Asegúrate de tener Python instalado.
2. Clona este repositorio en tu entorno local.
3. Navega a la carpeta del proyecto e instala cualquier dependencia requerida.
4. Ejecuta `Rasterizer.py` para cargar el modelo y generar la imagen con texturas aplicadas.
5. Las imágenes de salida se guardarán en formato BMP en la carpeta raíz del proyecto.

## Dependencias

Este proyecto no tiene dependencias externas adicionales.

## Contacto

Gabriel Paz 221087
UNIVERSIDAD DEL VALLE DE GUATEMALA
