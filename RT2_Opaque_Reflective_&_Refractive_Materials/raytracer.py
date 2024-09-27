# Universidad del Valle de Guatemala
# Graficas por Computadora
# Gabriel Alberto Paz González

# Raytracer.py

import pygame
from pygame.locals import *
from gl import RendererRT
from figures import Sphere
from material import *
from texture import Texture
from lights import AmbientLight, DirectionalLight

width = 250
height = 250

screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rt = RendererRT(screen)

rt.envMap = Texture("mapa.bmp")

piedra = Material(diffuse=[0.5, 0.5, 0.5], spec=5, Ks=0.0, matType=OPAQUE)  
ladrillo = Material(diffuse=[0.6, 0.1, 0.1], spec=15, Ks=0.0, matType=OPAQUE)

vidrio = Material(diffuse=[0.9, 0.9, 0.9], spec=32, Ks=0.05, ior=1.52, matType=TRANSPARENT)
agua = Material(diffuse=[0.5, 0.7, 0.9], spec=48, Ks=0.05, ior=1.33, matType=TRANSPARENT)

plata = Material(diffuse=[0.95, 0.95, 0.95], spec=200, Ks=0.8, matType=REFLECTIVE)
cobre = Material(diffuse=[0.9, 0.45, 0.25], spec=128, Ks=0.7, matType=REFLECTIVE)


rt.lights.append(DirectionalLight(direction=[0, -1, -1]))
rt.lights.append(AmbientLight(intensity=0.3))

rt.scene.append(Sphere(position=[0, 3, -10], radius=2.0, material=piedra))
rt.scene.append(Sphere(position=[0, -3, -10], radius=2.0, material=cobre))

rt.scene.append(Sphere(position=[-4, 3, -10], radius=2.0, material=plata))
rt.scene.append(Sphere(position=[-4, -3, -10], radius=2.0, material=agua))

rt.scene.append(Sphere(position=[4, 3, -10], radius=2.0, material=ladrillo))
rt.scene.append(Sphere(position=[4, -3, -10], radius=2.0, material=vidrio))


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
