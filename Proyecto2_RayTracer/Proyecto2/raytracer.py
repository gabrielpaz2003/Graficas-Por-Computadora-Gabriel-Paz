# Universidad del Valle de Guatemala
# Graficas por Computadora
# Gabriel Alberto Paz González

# Raytracer.py

import pygame
from pygame.locals import *
from gl import RendererRT
from figures import Sphere, Plane, Disk, Ellipsoid, Cylinder, Cone, Rectangle
from material import OPAQUE, REFLECTIVE, TRANSPARENT, Material
from texture import Texture
from lights import AmbientLight, DirectionalLight, PointLight, SpotLight

width = 600
height = 400

screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rt = RendererRT(screen)

rt.envMap = Texture("fondo.bmp")

piedra = Material(diffuse=[0.5, 0.5, 0.5], spec=5, Ks=0.0, matType=OPAQUE)
piedraAzul = Material(diffuse=[0.5, 0.7, 0.9], spec=64, Ks=0.05, ior=1.5, matType=TRANSPARENT)
piedraRoja = Material(diffuse=[0.5, 0.5, 0.5], spec=5, Ks=0.0, matType=OPAQUE, texture=Texture("pierdaR.bmp"))
arena = Material(diffuse=[0.5, 0.5, 0.5], spec=5, Ks=0.0, matType=OPAQUE, texture=Texture("arena.bmp"))
pina = Material(diffuse=[0.5, 0.5, 0.5], spec=5, Ks=0.0, matType=OPAQUE, texture=Texture("pina.bmp"))
ladrillo = Material(diffuse=[0.6, 0.1, 0.1], spec=15, Ks=0.0, matType=OPAQUE)

vidrio = Material(diffuse=[0.9, 0.9, 0.9], spec=32,
                  Ks=0.05, ior=1.52, matType=TRANSPARENT)
agua = Material(diffuse=[0.5, 0.7, 0.9], spec=48,
                Ks=0.05, ior=1.33, matType=TRANSPARENT)

plata = Material(diffuse=[0.95, 0.95, 0.95],
                 spec=200, Ks=0.8, matType=REFLECTIVE)
cobre = Material(diffuse=[0.9, 0.45, 0.25], spec=128,
                 Ks=0.7, matType=REFLECTIVE)

rt.lights.append(DirectionalLight(direction=[0, -1, -1]))
rt.lights.append(AmbientLight(intensity=0.3))
rt.lights.append(PointLight(position=[4.99, 5.99, -5], intensity=10))
rt.lights.append(
    SpotLight(position=[-1, 5.5, -7.5], direction=[0, -1, 0], intensity=10))


rt.scene.append(Ellipsoid(
    position=[-6, -2, -12],
    radii=[2, 2, 2],
    material=piedraRoja
))

rt.scene.append(Cylinder(
    position=[0, -3, -12],
    material=piedraAzul,
    radius=2,
    height=6
))

rt.scene.append(Ellipsoid(
    position=[0, 0, -8],
    radii=[0.5, 0.75, 0.5],
    material=piedra
))

rt.scene.append(Ellipsoid(
    position=[1, 1.5, -12],
    radii=[0.75, 0.75, 2],
    material=plata
))

rt.scene.append(Ellipsoid(
    position=[-1, 1.5, -12],
    radii=[0.75, 0.75, 2],
    material=plata
))

rt.scene.append(Cone(position=[6.4, 2, -12], radius=0.8, height=0.8, material=cobre))
rt.scene.append(Cone(position=[6, 2, -12], radius=1, height=1, material=cobre))
rt.scene.append(Cone(position=[5.5, 2, -12], radius=0.7, height=0.7, material=cobre))


rt.scene.append(Ellipsoid(
    position=[6, -1, -12],
    radii=[2, 3, 2],
    material=pina
))

rt.scene.append(Ellipsoid(
    position=[5.5, -0, -8],
    radii=[0.5, 0.75, 0.5],
    material=cobre
))


rt.scene.append(Rectangle(
    position=[0, -1, -1],
    normal=[0, 1, 0],
    width=8.0,
    height=7.5,
    material=arena
))

rt.glRender()


isRunning = True
while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
                rt.glGenerateFrameBuffer('output.bmp')
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
