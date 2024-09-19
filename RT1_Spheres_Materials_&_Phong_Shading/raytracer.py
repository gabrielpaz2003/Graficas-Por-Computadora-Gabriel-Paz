# Universidad del Valle de Guatemala
# Graficas por Computadora
# Gabriel Alberto Paz González

# Raytracer.py

import pygame
from pygame.locals import *
from gl import RendererRT
from figures import Sphere
from material import Material
from lights import AmbientLight, DirectionalLight

width = 720
height = 720

screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rt = RendererRT(screen)

nieve = Material(diffuse=[1, 1, 1], spec=32, Ks=0.05)
naranja = Material(diffuse=[1.0, 0.6, 0.0], spec=64, Ks=0.2)
negro = Material(diffuse=[0, 0, 0], spec=1.0, Ks=0.0)

rt.lights.append(DirectionalLight(direction=[0, -1, -1]))
rt.lights.append(AmbientLight(intensity=0.3))

rt.scene.append(Sphere(position=[0, -3, -10], radius=2.2, material=nieve))
rt.scene.append(Sphere(position=[0, 0, -10], radius=1.7, material=nieve))
rt.scene.append(Sphere(position=[0, 2.4, -10], radius=1.3, material=nieve))
rt.scene.append(Sphere(position=[0, -2.75, -8.0], radius=0.4, material=negro))
rt.scene.append(Sphere(position=[0, -1.25, -8.4], radius=0.4, material=negro))
rt.scene.append(Sphere(position=[0, 0.3, -8.55], radius=0.4, material=negro))
rt.scene.append(Sphere(position=[0, 2.4, -8.8], radius=0.2, material=naranja))

rt.scene.append(Sphere(position=[-0.5, 2.7, -8.8], radius=0.2, material=negro))
rt.scene.append(Sphere(position=[0.4, 2.7, -8.8], radius=0.2, material=negro))

rt.scene.append(Sphere(position=[0.225, 1.9, -8.8], radius=0.2, material=negro))
rt.scene.append(Sphere(position=[-0.225, 1.9, -8.8], radius=0.2, material=negro))
rt.scene.append(Sphere(position=[-0.6, 2.1, -8.8], radius=0.2, material=negro))
rt.scene.append(Sphere(position=[0.6, 2.1, -8.8], radius=0.2, material=negro))


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
