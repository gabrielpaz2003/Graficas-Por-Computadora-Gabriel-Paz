from intercept import Intercept
from mathl import *
from math import atan2, acos, pi, isclose


class Shape(object):
    def __init__(self, position, material):
        self.position = position
        self.material = material
        self.type = "None"

    def ray_intersect(self, orig, dir):
        return None


class Sphere(Shape):
    def __init__(self, position, radius, material):
        super().__init__(position, material)
        self.radius = radius
        self.type = "Sphere"

    def ray_intersect(self, orig, dir):
        # Vector substraction
        L = resta(self.position, orig)
        # Producto punto
        tca = dotProduct(L, dir)
        # np.linalg.norm = magnitud,
        d = (norm(L) ** 2 - tca ** 2) ** 0.5

        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d ** 2) ** 0.5

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1

        if t0 < 0:
            return None

        P = suma(orig, producto(dir, t0))
        normal = resta(P, self.position)
        normal = [a / norm(normal) for a in normal]

        u = (atan2(normal[2], normal[0])) / (2 * pi) + 0.5
        v = acos(-normal[1]) / pi

        return Intercept(point=P,
                         normal=normal,
                         distance=t0,
                         obj=self,
                         texCoords=[u, v],
                         rayDirection=dir
                         )


class Plane(Shape):
    def __init__(self, position, normal, material, texture_scale=(0.5, 0.5)):
        super().__init__(position, material)
        self.normal = [a / norm(normal) for a in normal]
        self.type = "Plane"
        self.u_dir, self.v_dir = compute_uv_axes(self.normal)
        self.texture_scale = texture_scale

    def ray_intersect(self, orig, dir):
        denom = dotProduct(dir, self.normal)
        if isclose(0, denom):
            return None

        num = dotProduct(resta(self.position, orig), self.normal)
        t = num / denom

        if t < 0:
            return None

        P = suma(orig, [a * t for a in dir])

        # Project P onto the plane's basis vectors to get texture coordinates
        local_p = resta(P, self.position)
        u = dotProduct(local_p, self.u_dir) * self.texture_scale[0]
        v = dotProduct(local_p, self.v_dir) * self.texture_scale[1]

        # Wrap the texture coordinates to be within [0, 1]
        u = u % 1.0
        v = v % 1.0

        return Intercept(
            point=P,
            normal=self.normal,
            distance=t,
            texCoords=[u, v],
            rayDirection=dir,
            obj=self,
        )


class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        super().__init__(position, normal, material)
        self.radius = radius
        self.type = "Disk"

    def ray_intersect(self, orig, dir):
        planeIntercept = super().ray_intersect(orig, dir)

        if planeIntercept is None:
            return None

        contact = resta(planeIntercept.point, self.position)

        contact = norm(contact)

        if contact > self.radius:
            return None

        return planeIntercept


class AABB(Shape):
    # Axis Aligned Bounding Box
    def __init__(self, position, sizes, material):
        super().__init__(position, material)
        self.sizes = sizes
        self.type = "AABB"

        self.planes = []

        rightPlane = Plane(
            [position[0] + sizes[0]/2, position[1], position[2]], [1, 0, 0], material)
        leftPlane = Plane(
            [position[0] - sizes[0]/2, position[1], position[2]], [-1, 0, 0], material)

        upPlane = Plane([position[0], position[1] + sizes[1] /
                        2, position[2]], [0, 1, 0], material)
        downPlane = Plane([position[0], position[1] -
                          sizes[1]/2, position[2]], [0, -1, 0], material)

        frontPlane = Plane(
            [position[0], position[1], position[2] + sizes[2]/2], [0, 0, 1], material)
        backPlane = Plane(
            [position[0], position[1], position[2] - sizes[2]/2], [0, 0, -1], material)

        self.planes.append(rightPlane)
        self.planes.append(leftPlane)
        self.planes.append(upPlane)
        self.planes.append(downPlane)
        self.planes.append(frontPlane)
        self.planes.append(backPlane)

        # Bounds

        self.boundsMin = [0, 0, 0]

        self.boundsMax = [0, 0, 0]

        epsilon = 0.001

        for i in range(3):
            self.boundsMin[i] = position[i] - (epsilon + sizes[i] / 2)
            self.boundsMax[i] = position[i] + (epsilon + sizes[i] / 2)

    def ray_intersect(self, orig, dir):
        intercept = None
        t = float("inf")
        for plane in self.planes:
            planeIntercept = plane.ray_intersect(orig, dir)

            if planeIntercept is not None:
                planePoint = planeIntercept.point

                if self.boundsMin[0] <= planePoint[0] <= self.boundsMax[0]:
                    if self.boundsMin[1] <= planePoint[1] <= self.boundsMax[1]:
                        if self.boundsMin[2] <= planePoint[2] <= self.boundsMax[2]:
                            if planeIntercept.distance < t:
                                t = planeIntercept.distance
                                intercept = planeIntercept

        if intercept == None:
            return None

        u, v = 0, 0

        if abs(intercept.normal[0]) > 0:
            u = (intercept.point[1] - self.boundsMin[1]) / self.sizes[1]
            v = (intercept.point[2] - self.boundsMin[2]) / self.sizes[2]

        elif abs(intercept.normal[1]) > 0:
            u = (intercept.point[0] - self.boundsMin[0]) / self.sizes[0]
            v = (intercept.point[2] - self.boundsMin[2]) / self.sizes[2]

        elif abs(intercept.normal[2]) > 0:
            u = (intercept.point[0] - self.boundsMin[0]) / self.sizes[0]
            v = (intercept.point[1] - self.boundsMin[1]) / self.sizes[1]

        u = min(0.999, max(0, u))
        v = min(0.999, max(0, v))

        return Intercept(point=intercept.point,
                         normal=intercept.normal,
                         distance=t,
                         texCoords=[u, v],
                         rayDirection=dir,
                         obj=self)

class Ellipsoid(Shape):
    def __init__(self, position, radii, material):
        super().__init__(position, material)
        self.radii = radii  # Los radios [rx, ry, rz] a lo largo de cada eje
        self.type = "Ellipsoid"

    def ray_intersect(self, orig, dir):
        # Escalar el rayo para transformar el elipsoide en una esfera
        scaled_origin = self.scale_point(orig, inverse=True)
        scaled_dir = self.scale_direction(dir, inverse=True)

        # Calcular la intersección del rayo con la esfera transformada (de radio 1)
        L = resta(self.scale_point(self.position, inverse=True), scaled_origin)
        tca = dotProduct(L, scaled_dir)
        d2 = dotProduct(L, L) - tca ** 2
        
        # Si la distancia es mayor que 1, no hay intersección (en el espacio de la esfera)
        if d2 > 1:
            return None
        
        thc = (1 - d2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc

        # Seleccionar la distancia de intersección más cercana (si está adelante del rayo)
        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None

        # Calcular el punto de intersección en el espacio escalado
        P_scaled = suma(scaled_origin, producto(t0, scaled_dir))
        
        # Transformar el punto de intersección de vuelta al espacio del elipsoide original
        P = self.scale_point(P_scaled, inverse=False)
        
        # Calcular la normal en el punto de intersección
        normal = resta(P, self.position)
        normal = self.scale_direction(normal, inverse=True)  # Transformar normal al espacio de la esfera
        normal = normalize(normal)  # Normalizar

        # Calcular coordenadas de textura (usando una proyección esférica simple)
        u = (atan2(normal[2], normal[0])) / (2 * pi) + 0.5
        v = acos(-normal[1]) / pi

        return Intercept(
            point=P,
            normal=normal,
            distance=t0,
            obj=self,
            texCoords=[u, v],
            rayDirection=dir
        )

    def scale_point(self, point, inverse=False):
        if inverse:
            # Transformar al espacio de la esfera (inverso de los radios)
            return [point[0] / self.radii[0], point[1] / self.radii[1], point[2] / self.radii[2]]
        else:
            # Transformar al espacio del elipsoide
            return [point[0] * self.radii[0], point[1] * self.radii[1], point[2] * self.radii[2]]

    def scale_direction(self, direction, inverse=False):
        if inverse:
            # Transformar al espacio de la esfera (inverso de los radios)
            return normalize([direction[0] / self.radii[0], direction[1] / self.radii[1], direction[2] / self.radii[2]])
        else:
            # Transformar al espacio del elipsoide
            return normalize([direction[0] * self.radii[0], direction[1] * self.radii[1], direction[2] * self.radii[2]])

