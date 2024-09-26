import struct
from camera import Camera
from mathl import barycentricCoords
from math import tan, pi, isclose


def char(c):
    # 1 byte
    return struct.pack("=c", c.encode("ascii"))


def word(w):
    # 2 bytes
    return struct.pack("=h", w)


def dword(d):
    # 4 bytes
    return struct.pack("=l", d)


POINTS = 0
LINES = 1
TRIANGLES = 2


class Renderer(object):
    def __init__(self, screen):

        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        self.camera = Camera()
        self.glViewport(0, 0, self.width, self.height)
        self.glProjection()

        self.glColor(1, 1, 1)
        self.glClearColor(0, 0, 0)
        self.glClear()

        self.vertexShader = None
        self.fragmentShader = None

        self.activeTexture = None

        self.primitiveType = TRIANGLES

        self.models = []

    def glViewport(self, x, y, width, height):
        self.vpX = int(x)
        self.vpY = int(y)
        self.vpWidth = width
        self.vpHeight = height

        self.viewportMatrix = [[width/2, 0, 0, x + width/2],
                               [0, height/2, 0, y + height/2],
                               [0, 0, 0.5, 0.5],
                               [0, 0, 0, 1]]

    def glProjection(self, n=0.1, f=1000, fov=60):

        aspectRatio = self.vpWidth / self.vpHeight
        fov *= pi/180  # A radianes
        t = tan(fov / 2) * n
        r = t * aspectRatio

        self.projectionMatrix = [[n/r, 0, 0, 0],
                                [0, n/t, 0, 0],
                                [0, 0, -(f+n)/(f-n), -(2*f*n)/(f-n)],
                                [0, 0, -1, 0]]

    def glColor(self, r, g, b):
        r = min(1, max(0, r))
        g = min(1, max(0, g))
        b = min(1, max(0, b))

        self.currColor = [r, g, b]

    def glClearColor(self, r, g, b):
        r = min(1, max(0, r))
        g = min(1, max(0, g))
        b = min(1, max(0, b))

        self.clearColor = [r, g, b]

    def glClear(self):
        color = [int(i * 255) for i in self.clearColor]
        self.screen.fill(color)

        self.frameBuffer = [[self.clearColor for y in range(self.height)]
                            for x in range(self.width)]

        self.zbuffer = [[float('inf') for y in range(self.height)]
                        for x in range(self.width)]

    def glPoint(self, x, y, color=None):
        # Pygame empieza a renderizar desde la esquina
        # superior izquierda. Hay que voltear el valor y
        x = round(x)
        y = round(y)

        if (0 <= x < self.width) and (0 <= y < self.height):
            # Pygame recibe los colores en un rango de 0 a 255
            color = [int(i * 255) for i in (color or self.currColor)]
            self.screen.set_at((x, self.height - 1 - y), color)

            self.frameBuffer[x][y] = color

    def glLine(self, v0, v1, color=None):
        # y = mx + b

        x0 = v0[0]
        x1 = v1[0]
        y0 = v0[1]
        y1 = v1[1]

        # Algoritmo de Lineas de Bresenham

        # Si el punto 0 es igual al punto 1, solamente dibujo un punto
        if x0 == x1 and y0 == y1:
            self.glPoint(x0, y0)
            return

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0
        limit = 0.75
        m = dy / dx
        y = y0

        for x in range(round(x0), round(x1) + 1):
            if steep:
                self.glPoint(y, x, color or self.currColor)
            else:
                self.glPoint(x, y, color or self.currColor)

            offset += m

            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1

                limit += 1

    def glGenerateFrameBuffer(self, filename):

        with open(filename, "wb") as file:
            # Header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            # Info Header
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Color table
            for y in range(self.height):
                for x in range(self.width):
                    color = self.frameBuffer[x][y]
                    color = bytes([color[2],
                                   color[1],
                                   color[0]])

                    file.write(color)

    def glRender(self):

        for model in self.models:
            # Por cada modelo en la lista, los dibujo
            # Agarrar su matriz modelo
            mMat = model.GetModelMatrix()

            # Guardar la referencia a la textura de este modelo
            self.activeTexture = model.texture

            # Aqui vamos a guardar todos los vertices y su info correspondiente
            vertexBuffer = []

            # Para cada cara del modelo, recorremos la info de v�rtices de esa cara
            for face in model.faces:

                # Aqui vamos a guardar los vertices de esta cara
                faceVerts = []

                for i in range(len(face)):

                    # Aqui vamos a guardar los valores individuales de
                    # posicion, coordenadas de textura y normales
                    vert = []

                    # Obtenemos los vertices de la cara actual
                    pos = model.vertices[face[i][0] - 1]

                    # Si contamos con un Vertex Shader, se manda cada vertice
                    # para transformalos. Recordar pasar las matrices necesarias
                    # para usarlas dentro del shader
                    if self.vertexShader:
                        pos = self.vertexShader(pos,
                                                modelMatrix=mMat,
                                                viewMatrix=self.camera.GetViewMatrix(),
                                                projectionMatrix=self.projectionMatrix,
                                                viewportMatrix=self.viewportMatrix)

                    # Agregamos los valores de posicion al contenedor del vertice
                    for value in pos:
                        vert.append(value)

                    # Obtenemos las coordenadas de textura de la cara actual
                    vts = model.texCoords[face[i][1] - 1]

                    # Agregamos los valores de vts al contenedor del vertice
                    for value in vts:
                        vert.append(value)

                    # Agregamos la informacion de este vertices a la
                    # lista de vertices de esta cara
                    faceVerts.append(vert)

                # Agregamos toda la informacion de los tres vertices de
                # esta cara de corrido al buffer de vertices. Si hay
                # cuatro vertices, creamos un segundo triangulo
                for value in faceVerts[0]:
                    vertexBuffer.append(value)
                for value in faceVerts[1]:
                    vertexBuffer.append(value)
                for value in faceVerts[2]:
                    vertexBuffer.append(value)
                if len(faceVerts) == 4:
                    for value in faceVerts[0]:
                        vertexBuffer.append(value)
                    for value in faceVerts[2]:
                        vertexBuffer.append(value)
                    for value in faceVerts[3]:
                        vertexBuffer.append(value)

            # Mandamos el buffer de vertices de este modelo a ser dibujado
            self.glDrawPrimitives(vertexBuffer, 5)

    def glTriangle(self, A, B, C):
        minX = round(min(A[0], B[0], C[0]))
        minY = round(min(A[1], B[1], C[1]))
        maxX = round(max(A[0], B[0], C[0]))
        maxY = round(max(A[1], B[1], C[1]))

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                P = [x, y]
                if barycentricCoords(A, B, C, P) != None:
                    self.glDrawTrianglePoint(A, B, C, P)

    def glTriangle_std(self, A, B, C):

        # Hay que asegurar que los vertices entran
        # en orden: Ay > By > Cy
        if A[1] < B[1]:
            A, B = B, A
        if A[1] < C[1]:
            A, C = C, A
        if B[1] < C[1]:
            B, C = C, B

        def flatBottom(vA, vB, vC):

            try:
                mBA = (vB[0] - vA[0]) / (vB[1] - vA[1])
                mCA = (vC[0] - vA[0]) / (vC[1] - vA[1])
            except:
                pass
            else:
                if vB[0] > vC[0]:
                    vB, vC = vC, vB

                x0 = vB[0]
                x1 = vC[0]

                for y in range(round(vB[1]), round(vA[1] + 1)):
                    for x in range(round(x0 - 1), round(x1 + 1)):
                        vP = [x, y]
                        self.glDrawTrianglePoint(vA, vB, vC, vP)

                    x0 += mBA
                    x1 += mCA

        def flatTop(vA, vB, vC):

            try:
                mCA = (vC[0] - vA[0]) / (vC[1] - vA[1])
                mCB = (vC[0] - vB[0]) / (vC[1] - vB[1])
            except:
                pass
            else:
                if vA[0] > vB[0]:
                    vA, vB = vB, vA

                x0 = vA[0]
                x1 = vB[0]

                for y in range(round(vA[1]), round(vC[1] - 1), -1):
                    for x in range(round(x0 - 1), round(x1 + 1)):
                        vP = [x, y]
                        self.glDrawTrianglePoint(vA, vB, vC, vP)

                    x0 -= mCA
                    x1 -= mCB

        if B[1] == C[1]:
            # Si el punto B y C estan a la misma altura,
            # se dibuja un triangulo con parte plana abajo
            flatBottom(A, B, C)

        elif A[1] == B[1]:
            # Si el punto A y B estan a la misma altura,
            # se dibuja un triangulo con parte plana arriba
            flatTop(A, B, C)

        else:
            # Divido el triangulo en dos partes y dibujo ambos tipos de triangulos
            # Teorema del intercepto para calcular D en X y Y
            D = [A[0] + ((B[1] - A[1]) / (C[1] - A[1])) * (C[0] - A[0]), B[1]]

            u, v, w = barycentricCoords(A, B, C, D)

            for i in range(2, len(A)):
                # P = uA + vB + wC
                D.append(u * A[i] + v * B[i] + w * C[i])

            flatBottom(A, B, D)
            flatTop(B, D, C)

    def glDrawTrianglePoint(self, A, B, C, P):

        x = P[0]
        y = P[1]

        # Si el punto no esta dentro de la ventana, lo descartamos
        if not (0 <= x < self.width) or not (0 <= y < self.height):
            return

        # Obtenemos las coordenadas baricentricas del punto P
        # en este triangulo. Si no son validas, no dibujamos
        bCoords = barycentricCoords(A, B, C, P)

        if bCoords == None:
            return

        u, v, w = bCoords

        # Hay que asegurarse que la suma de las coordenadas baricentricas es igual a 1
        if not isclose(u + v + w, 1.0):
            return

        # Se calcula el valor de Z de este pixerl especifico

        z = u * A[2] + v * B[2] + w * C[2]

        # Si el valor de Z para este punto es mayor que el valor guardado
        # en el Zbuffer, este punto esta mas lejos y no se dibuja
        if z >= self.zbuffer[x][y]:
            return

        self.zbuffer[x][y] = z

        # Si contamos un Fragment Shader, obtener el color de ah�
        color = self.currColor

        if self.fragmentShader != None:
            # Mandar los par�metros necesarios al shader
            verts = (A, B, C)
            color = self.fragmentShader(verts=verts,
                                        bCoords=bCoords,
                                        texture=self.activeTexture)

        self.glPoint(x, y, color)

    def glDrawPrimitives(self, buffer, vertexOffset):
        # El buffer es un listado de valores que representan
        # toda la informacion de un vertice (posicion, coordenadas
        # de textura, normales, color, etc.). El VertexOffset se
        # refiere a cada cuantos valores empieza la informacion
        # de un vertice individual
        # Se asume que los primeros tres valores de un vertice
        # corresponden a Posicion.

        if self.primitiveType == POINTS:

            # Si son puntos, revisamos el buffer en saltos igual
            # al Vertex Offset. El valor X y Y de cada vertice
            # corresponden a los dos primeros valores.
            for i in range(0, len(buffer), vertexOffset):
                x = buffer[i]
                y = buffer[i + 1]
                self.glPoint(x, y)

        elif self.primitiveType == LINES:

            # Si son lineas, revisamos el buffer en saltos igual
            # a 3 veces el Vertex Offset, porque cada trio corresponde
            # a un triangulo.
            for i in range(0, len(buffer), vertexOffset * 3):
                for j in range(3):
                    # Hay que dibujar la linea de un vertice al siguiente
                    x0 = buffer[i + vertexOffset * j + 0]
                    y0 = buffer[i + vertexOffset * j + 1]

                    # En caso de que sea el ultimo vertices, el siguiente
                    # seria el primero
                    x1 = buffer[i + vertexOffset * ((j + 1) % 3) + 0]
                    y1 = buffer[i + vertexOffset * ((j + 1) % 3) + 1]

                    self.glLine((x0, y0), (x1, y1))

        elif self.primitiveType == TRIANGLES:

            # Si son triangulos revisamos el buffer en saltos igual
            # a 3 veces el Vertex Offset, porque cada trio corresponde
            # a un triangulo.
            for i in range(0, len(buffer), vertexOffset * 3):

                # Necesitamos tres vertices para mandar a dibujar el triangulo.
                # Cada vertice necesita todos sus datos, la cantidad de estos
                # datos es igual a VertexOffset
                A = [buffer[i + j + vertexOffset * 0]
                     for j in range(vertexOffset)]
                B = [buffer[i + j + vertexOffset * 1]
                     for j in range(vertexOffset)]
                C = [buffer[i + j + vertexOffset * 2]
                     for j in range(vertexOffset)]

                self.glTriangle(A, B, C)
