
# Laboratorio 2 - Shaders y Modelos 3D

Este proyecto de laboratorio introduce el uso de shaders para mejorar el realismo de los modelos 3D renderizados. Los shaders permiten modificar las propiedades de la iluminación y el color de los modelos, agregando efectos visuales más detallados y personalizados. El proyecto está desarrollado en Python y utiliza módulos personalizados para cargar, transformar y renderizar modelos 3D con soporte para shaders.

## Contenido del Proyecto

El proyecto contiene los siguientes archivos:

### Archivos de Código:
- **camera.py**: Maneja los ángulos de la cámara y la perspectiva para visualizar el modelo 3D.
- **gl.py**: Coordina el rasterizador y las operaciones necesarias para generar imágenes BMP con soporte para shaders.
- **mathl.py**: Funciones matemáticas que se utilizan para las transformaciones de vectores y matrices.
- **model.py**: Administra la carga, manipulación y transformación de los modelos 3D.
- **obj.py**: Utilidades para cargar archivos `.obj` y prepararlos para el renderizado.
- **Rasterizer.py**: Coordina el proceso de renderizado del modelo y la aplicación de shaders.
- **shaders.py**: Contiene la lógica para la aplicación de shaders sobre los modelos 3D.
- **texture.py**: Administra la carga y mapeo de texturas sobre los modelos.

### Archivos de Imágenes y Modelos:
- **barril.obj**: El modelo 3D utilizado en el laboratorio.
- **barril.bmp**: Imagen del modelo renderizado con shaders.
- **output.bmp**: Imagen final generada por el rasterizador.

### Otros Archivos:
- **README.md**: Este archivo de documentación.

## Cómo Ejecutar el Proyecto

1. Asegúrate de tener Python instalado en tu sistema.
2. Clona este repositorio en tu entorno local.
3. Navega a la carpeta del proyecto e instala cualquier dependencia adicional si es necesario.
4. Ejecuta `Rasterizer.py` para cargar el modelo y generar la imagen con shaders aplicados.
5. Las imágenes de salida se guardarán en formato BMP en la carpeta raíz del proyecto.

## Dependencias

Este proyecto no tiene dependencias externas adicionales más allá de Python.

## Contacto

Gabriel Paz 221087
UNIVERSIDAD DEL VALLE DE GUATEMALA
