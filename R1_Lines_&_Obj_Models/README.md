
# R1 Lines & Obj Models

Este proyecto es una implementación de un rasterizador para cargar, manipular y renderizar modelos 3D en formato `.obj`, así como la generación de imágenes en formato BMP. Está desarrollado en Python y utiliza varios módulos personalizados para manejar las operaciones gráficas y matemáticas necesarias.

## Contenido del Proyecto

El proyecto contiene los siguientes archivos:

### Archivos de Código:
- **gl.py**: Este archivo contiene la lógica principal para el rasterizador y las operaciones gráficas básicas, como la inicialización del frame buffer, dibujado de líneas y la generación de imágenes BMP.
- **mathl.py**: Contiene las funciones matemáticas necesarias para la manipulación de matrices y vectores en 3D.
- **model.py**: Se encarga de manejar los modelos 3D, cargarlos desde un archivo `.obj`, y aplicar las transformaciones correspondientes.
- **obj.py**: Este archivo contiene las utilidades para cargar y leer archivos `.obj` y convertirlos en representaciones utilizables por el rasterizador.
- **Rasterizer.py**: Coordina el proceso de rasterización, desde la carga del modelo hasta la renderización en una imagen BMP.
- **shaders.py**: Contiene las funciones relacionadas con el sombreado de los objetos en la escena.

### Archivos de Entrada y Salida:
- **pez.obj**: Archivo del modelo 3D utilizado en este proyecto.
- **pez.bmp**: Imagen de salida generada por el rasterizador en formato BMP.
- **pez.jpg**: Representación en formato JPG del modelo.

### Otros Archivos:
- **output.bmp**: Imagen de salida generada por el proyecto.
- **README.md**: Este archivo de documentación.

## Cómo Ejecutar el Proyecto

1. Asegúrate de tener Python instalado en tu máquina.
2. Clona este repositorio en tu entorno local.
3. Navega a la carpeta del proyecto e instala las dependencias necesarias.
4. Ejecuta `Rasterizer.py` para cargar el modelo y generar la imagen de salida en formato BMP.

## Dependencias

Este proyecto no tiene dependencias externas específicas, ya que todo se implementa de forma nativa en Python.

## Contacto

Gabriel Paz 221087
UNIVERSIDAD DEL VALLE DE GUATEMALA
