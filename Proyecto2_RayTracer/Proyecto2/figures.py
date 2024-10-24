from intercept import Intercept
from mathl import dotProduct, resta, producto, suma, norm, compute_uv_axes, normalize, cross_product
from math import atan2, acos, pi, isclose, sin, cos
from random import random


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
        # Transformar normal al espacio de la esfera
        normal = self.scale_direction(normal, inverse=True)
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


class Cylinder(Shape):
    def __init__(self, position, radius, height, material):
        super().__init__(position, material)
        self.radius = radius
        self.height = height
        self.type = "Cylinder"

    def ray_intersect_body(self, orig, dir):
        dx, dz = dir[0], dir[2]
        ox, oz = orig[0] - self.position[0], orig[2] - self.position[2]

        # Resolver intersección con un cilindro en xz (ignorar y por ahora)
        a = dx * dx + dz * dz
        b = 2 * (ox * dx + oz * dz)
        c = ox * ox + oz * oz - self.radius ** 2

        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return None  # No hay intersección con el cuerpo del cilindro

        sqrt_disc = (discriminant)**(0.5)
        t0 = (-b - sqrt_disc) / (2 * a)
        t1 = (-b + sqrt_disc) / (2 * a)

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None

        # Calcular el punto de intersección
        P = suma(orig, producto(t0, dir))

        # Verificar si el punto está dentro de la altura del cilindro
        if self.position[1] <= P[1] <= (self.position[1] + self.height):
            normal = [P[0] - self.position[0], 0, P[2] - self.position[2]]
            normal = normalize(normal)

            # Calcular las coordenadas de textura
            u = (atan2(normal[2], normal[0])) / (2 * pi) + 0.5
            v = (P[1] - self.position[1]) / self.height

            return Intercept(
                point=P,
                normal=normal,
                distance=t0,
                texCoords=[u, v],
                obj=self,
                rayDirection=dir
            )

        # Si no está dentro de la altura, no hay intersección con el cuerpo
        return None

    def ray_intersect_caps(self, orig, dir):
        # Verificar intersección con la tapa inferior
        base_cap = Disk(self.position, [0, 1, 0], self.radius, self.material)
        bottom_intercept = base_cap.ray_intersect(orig, dir)

        # Verificar intersección con la tapa superior
        top_cap_position = [self.position[0],
                            self.position[1] + self.height, self.position[2]]
        top_cap = Disk(top_cap_position, [0, 1, 0], self.radius, self.material)
        top_intercept = top_cap.ray_intersect(orig, dir)

        # Retornar la intersección más cercana
        if bottom_intercept and top_intercept:
            return bottom_intercept if bottom_intercept.distance < top_intercept.distance else top_intercept
        return bottom_intercept or top_intercept

    def ray_intersect(self, orig, dir):
        body_intercept = self.ray_intersect_body(orig, dir)
        caps_intercept = self.ray_intersect_caps(orig, dir)

        # Retornar la intersección más cercana entre el cuerpo y las tapas
        if body_intercept and caps_intercept:
            return body_intercept if body_intercept.distance < caps_intercept.distance else caps_intercept
        return body_intercept or caps_intercept

class Cone(Shape):
    def __init__(self, position, radius, height, material):
        super().__init__(position, material)
        self.radius = radius
        self.height = height
        self.type = "Cone"

    def ray_intersect_body(self, orig, dir):
        x0, y0, z0 = self.position
        dx, dy, dz = dir
        ox, oy, oz = resta(orig, self.position)

        k = self.radius / self.height
        k = k * k

        A = dx * dx + dz * dz - k * dy * dy
        B = 2 * (ox * dx + oz * dz - k * oy * dy)
        C = ox * ox + oz * oz - k * oy * oy

        discriminant = B * B - 4 * A * C

        if discriminant < 0 or isclose(A, 0):
            return None

        sqrt_disc = discriminant ** 0.5
        t0 = (-B - sqrt_disc) / (2 * A)
        t1 = (-B + sqrt_disc) / (2 * A)

        if t0 > t1:
            t0, t1 = t1, t0

        y = oy + dy * t0
        if t0 >= 0 and y >= 0 and y <= self.height:
            P = suma(orig, producto(dir, t0))
            normal = resta(P, self.position)
            normal[1] = - (self.radius / self.height) * norm([normal[0], normal[2]])
            normal = normalize(normal)

            phi = atan2(normal[2], normal[0])
            u = (phi / (2 * pi)) + 0.5
            v = y / self.height

            return Intercept(
                point=P,
                normal=normal,
                distance=t0,
                texCoords=[u, v],
                obj=self,
                rayDirection=dir
            )

        y = oy + dy * t1
        if t1 >= 0 and y >= 0 and y <= self.height:
            P = suma(orig, producto(dir, t1))
            normal = resta(P, self.position)
            normal[1] = - (self.radius / self.height) * norm([normal[0], normal[2]])
            normal = normalize(normal)

            phi = atan2(normal[2], normal[0])
            u = (phi / (2 * pi)) + 0.5
            v = y / self.height

            return Intercept(
                point=P,
                normal=normal,
                distance=t1,
                texCoords=[u, v],
                obj=self,
                rayDirection=dir
            )

        return None

    def ray_intersect_base(self, orig, dir):
        y_base = self.position[1] + self.height
        base_center = [self.position[0], y_base, self.position[2]]
        base_normal = [0, -1, 0]
        base_disk = Disk(base_center, base_normal, self.radius, self.material)
        return base_disk.ray_intersect(orig, dir)

    def ray_intersect(self, orig, dir):
        body_hit = self.ray_intersect_body(orig, dir)
        base_hit = self.ray_intersect_base(orig, dir)

        if body_hit and base_hit:
            if body_hit.distance < base_hit.distance:
                return body_hit
            else:
                return base_hit
        elif body_hit:
            return body_hit
        elif base_hit:
            return base_hit
        else:
            return None



class Rectangle(Shape):
    def __init__(self, position, normal, width, height, material):
        super().__init__(position, material)
        self.normal = normalize(normal)
        self.width = width
        self.height = height
        self.type = "Rectangle"

        # Compute the local axes for texture mapping and boundaries
        self.u_dir, self.v_dir = self.compute_uv_axes(self.normal)

        # Compute the half-sizes for easy boundary checking
        self.half_width = width / 2
        self.half_height = height / 2

    def compute_uv_axes(self, normal):
        """Compute two orthogonal unit vectors to the given normal."""
        # If the normal is near the Y axis, use Z and X for orthogonal directions
        if isclose(abs(normal[1]), 1.0):
            u = normalize([1, 0, 0])
        else:
            u = normalize([-normal[2], 0, normal[0]])
        v = normalize(cross_product(normal, u))
        return u, v

    def ray_intersect(self, orig, dir):
        denom = dotProduct(dir, self.normal)
        if isclose(denom, 0.0):
            return None  # Ray is parallel to the rectangle

        # Calculate intersection point with the plane containing the rectangle
        t = dotProduct(resta(self.position, orig), self.normal) / denom
        if t < 0:
            return None  # Intersection is behind the ray origin

        # Calculate the intersection point
        P = suma(orig, producto(dir, t))

        # Project the intersection point onto the local axes
        local_p = resta(P, self.position)
        u = dotProduct(local_p, self.u_dir)
        v = dotProduct(local_p, self.v_dir)

        # Check if the intersection point is within the rectangle boundaries
        if abs(u) > self.half_width or abs(v) > self.half_height:
            return None  # Intersection is outside the rectangle

        # Map the intersection point to UV texture coordinates
        u_tex = (u / self.width) + 0.5
        v_tex = (v / self.height) + 0.5

        return Intercept(
            point=P,
            normal=self.normal,
            distance=t,
            texCoords=[u_tex, v_tex],
            rayDirection=dir,
            obj=self
        )
