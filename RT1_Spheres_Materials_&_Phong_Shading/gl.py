import struct
from camera import Camera
from math import tan, pi
import pygame
import random
from mathl import norm


def char(c):
    # 1 byte
    return struct.pack("=c", c.encode("ascii"))


def word(w):
    # 2 bytes
    return struct.pack("=h", w)


def dword(d):
    # 4 bytes
    return struct.pack("=l", d)


class RendererRT(object):
    def __init__(self, screen):

        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        self.camera = Camera()
        self.glViewport(0, 0, self.width, self.height)
        self.glProjection()

        self.glColor(1, 1, 1)
        self.glClearColor(0, 0, 0)
        self.glClear()

        self.scene = []
        self.lights = []

    def glViewport(self, x, y, width, height):
        self.vpX = int(x)
        self.vpY = int(y)
        self.vpWidth = width
        self.vpHeight = height

    def glProjection(self, n=0.1, f=1000, fov=60):
        self.nearPlane = n
        self.farPlane = f
        self.fov = fov * pi / 180

        aspectRatio = self.vpWidth / self.vpHeight

        self.topEdge = tan(self.fov / 2) * self.nearPlane
        self.rightEdge = self.topEdge * aspectRatio

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

    def glCastRay(self, orig, direction, sceneObj=None):

        depth = float('inf')

        intercept = None
        hit = None

        for obj in self.scene:
            if obj != sceneObj:
                intercept = obj.ray_intersect(orig, direction)
                if intercept is not None:
                    if intercept.distance < depth:
                        hit = intercept
                        depth = intercept.distance

        return hit

    def glRender(self):

        indeces = [(i, j) for i in range(self.vpWidth)
                   for j in range(self.vpHeight)]
        random.shuffle(indeces)

        # for x in range(self.vpX, self.vpX + self.vpWidth):
        # 	for y in range(self.vpY, self.vpY + self.vpHeight):
        for i, j in indeces:
            x = i + self.vpX
            y = j + self.vpY
            if 0 <= x < self.width and 0 <= y < self.height:
                # Coordenadas normalizadas
                # Que van de -1 a 1

                pX = ((x + 0.5 - self.vpX) / self.vpWidth) * 2 - 1
                pY = ((y + 0.5 - self.vpY) / self.vpHeight) * 2 - 1

                pX *= self.rightEdge
                pY *= self.topEdge

                dir = [pX, pY, -self.nearPlane]
                dir = [(a / norm(dir)) for a in dir]

                intercept = self.glCastRay(self.camera.translate, dir)

                if intercept is not None:
                    color = intercept.obj.material.GetSurfaceColor(
                        intercept, self)
                    self.glPoint(x, y, color)
                    pygame.display.flip()
