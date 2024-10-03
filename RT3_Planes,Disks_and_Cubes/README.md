


# Proyecto de Trazado de Rayos en Python

Este laboratorio es un renderizador basado en trazado de rayos hecho en Python que crea escenas 3D con esferas y efectos básicos de iluminación. La implementación utiliza módulos personalizados para gestionar geometría, iluminación, materiales y renderizado.

## Tabla de Contenidos
- [Uso](#uso)
- [Módulos](#módulos)
- [Características](#características)
- [Ejemplo](#ejemplo)
- [Dependencias](#dependencias)
- [Licencia](#licencia)

   ```

## Uso

Para ejecutar el trazador de rayos, simplemente ejecuta el siguiente comando:
```bash
python raytracer.py
```

El resultado generará un archivo `.bmp` de la escena renderizada.

## Módulos

### 1. `camera.py`
Gestiona las operaciones de la cámara y las transformaciones de matriz para la escena 3D.

### 2. `figures.py`
Define formas geométricas como la `Esfera`. También maneja las intersecciones entre rayos y objetos necesarias para el renderizado.

### 3. `gl.py`
Implementa las funciones principales de renderizado y la generación del buffer de fotogramas.

### 4. `intercept.py`
Gestiona las intersecciones entre rayos y objetos y proporciona estructuras de datos para manejar puntos de impacto y normales.

### 5. `lights.py`
Define tipos de iluminación como la luz ambiental y direccional, que afectan la apariencia de los objetos en la escena.

### 6. `material.py`
Define materiales con propiedades como difusa, especular y reflexión para simular iluminación realista.

### 7. `mathl.py`
Proporciona funciones utilitarias para cálculos de vectores, como productos punto, resta de vectores y normas.

### 8. `model.py`
Gestiona modelos 3D y la carga de objetos (por ejemplo, archivos `.obj`) para renderizar formas complejas.

### 9. `obj.py`
Gestiona la carga y el análisis de archivos de modelo `.obj`.

### 10. `raytracer.py`
El script principal para configurar la escena, agregar objetos, luces y ejecutar el algoritmo de trazado de rayos.

## Características

- **Trazado de Rayos**: Un motor de trazado de rayos simple que calcula las intersecciones entre rayos y objetos en la escena.
- **Formas Básicas**: Soporta objetos esféricos.
- **Iluminación**: Implementa iluminación direccional y ambiental.
- **Materiales**: Soporta materiales con varias propiedades como reflexión difusa y especular.
- **Salida**: Renderiza imágenes como archivos `.bmp`.

## Ejemplo

Ejecutar el script renderizará una escena 3D con esferas e iluminación básica. Aquí hay un ejemplo de cómo se configura la escena en `raytracer.py`:

```python
from gl import RendererRT
from figures import Sphere
from material import Material
from lights import AmbientLight, DirectionalLight

# Configuración de la escena
rt = RendererRT(screen)
rt.lights.append(DirectionalLight(direction=[0, -1, -1]))
rt.scene.append(Sphere(position=[0, -3, -10], radius=2.2, material=Material(diffuse=[1, 1, 1])))
```

## Dependencias

- `pygame`: Para renderizar la escena en una pantalla y manejar eventos de ventana.
- `struct`: Para empaquetar datos en formatos binarios.
- `math`: Proporciona funciones matemáticas necesarias para el trazado de rayos.

Puedes instalar las dependencias usando `pip`:
```bash
pip install pygame
```

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
