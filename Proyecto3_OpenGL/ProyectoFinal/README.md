
# Proyecto: Motor de Renderizado 3D con Pygame

## Descripción

Este proyecto implementa un motor de renderizado 3D utilizando **Pygame** y **OpenGL**. Permite visualizar modelos 3D con texturas aplicadas, control de cámara, efectos de shaders y un entorno de skybox. El motor es interactivo y se puede controlar con el teclado y el mouse para navegar por la escena y cambiar entre diferentes shaders y modos de visualización.

---

## Características Principales

1. **Skybox**: Representa un fondo 3D utilizando texturas que simulan un entorno realista.
2. **Modelos 3D**: Carga modelos en formato `.obj` con texturas en formato `.bmp`.
3. **Shaders Personalizables**: Soporte para múltiples shaders, incluidos:
   - Texturas desplazables.
   - Inversión de colores.
   - Escala de grises.
   - Rotación dinámica.
   - Efectos de explosión y ondulación.
4. **Cámara Interactiva**:
   - Movimiento de cámara en órbita con controles de zoom y ángulo.
   - Foco automático en el modelo seleccionado.
5. **Controles de Usuario**:
   - Cambio entre modos de renderizado: sólido o alámbrico.
   - Interacción con el mouse para rotar la vista.
   - Navegación entre modelos de la escena.
6. **Música de Fondo**: Integración de un archivo `.mp3` para ambientar la escena.

---

## Requisitos del Sistema

- **Python 3.8+**
- **Pygame**
- **OpenGL**
- **Archivos de modelos `.obj`** y texturas correspondientes en formato `.bmp`.
- Archivos de shaders personalizados.

---

## Estructura del Proyecto

```
/
├── main.py                # Archivo principal de ejecución.
├── gl.py                  # Motor de renderizado y configuración de OpenGL.
├── buffer.py              # Manejo de buffers para modelos y texturas.
├── shaders.py             # Shaders personalizados (vértices y fragmentos).
├── model.py               # Clase para cargar y manejar modelos 3D.
├── textures/              # Texturas para los modelos y skybox.
├── models/                # Archivos `.obj` de los modelos 3D.
├── musica.mp3             # Música de fondo.
└── README.md              # Documentación del proyecto.
```

---

## Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone <repositorio_url>
   cd <nombre_del_proyecto>
   ```

2. **Instalar dependencias**:
   Asegúrate de tener instalado `pip`. Luego, instala las dependencias con:
   ```bash
   pip install pygame PyOpenGL
   ```

3. **Ejecutar el proyecto**:
   ```bash
   python main.py
   ```

---

## Controles

### Teclado:
- `ESC`: Salir de la aplicación.
- `1`: Modo de relleno sólido.
- `2`: Modo alámbrico.
- `3-9`: Cambiar shaders aplicados.
- `W/S`: Acercar/alejar cámara (zoom).
- `↑/↓`: Mover cámara en eje vertical.

### Mouse:
- **Click Izquierdo**: Arrastrar para rotar la vista.
- **Click Derecho**: Cambiar entre modelos en la escena.

---

## Créditos

- **Autor**: Gabriel Alberto Paz Gonzalez
- **Universidad del Valle de Guatemala**
- **Curso**: Gráficos por Computadora
- **Año**: 2024

---

## Notas

- Asegúrate de que las texturas y modelos se encuentren en las carpetas correspondientes.
- Si necesitas agregar modelos, utiliza archivos `.obj` y texturas en formato `.bmp`.
- Puedes personalizar los shaders en el archivo `shaders.py`.

---

## Licencia

Este proyecto está disponible bajo la licencia MIT. Puedes usarlo y modificarlo libremente para tus propios proyectos.
