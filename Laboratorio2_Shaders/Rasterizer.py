
import pygame
from pygame.locals import *
from gl import Renderer, POINTS, TRIANGLES, LINES
from model import Model
from shaders import (vertexShader,
                     noiseShader,
                     fragmentShader,
                     normalMappingShader,
                     fireShader
                     )
width = 900 
height = 600

screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.vertexShader = vertexShader
rend.fragmentShader = fragmentShader


modelo3 = Model("barril/barril.obj")
modelo3.LoadTexture("barril/barril.bmp")
modelo3.translate[0] = 25
modelo3.translate[1] = 12
modelo3.translate[2] = -80

modelo3.rotate[0] = 0
modelo3.rotate[1] = 180
modelo3.rotate[2] = 180

modelo3.scale[0] = 5
modelo3.scale[1] = 5
modelo3.scale[2] = 5
modelo3.vertexShader = vertexShader
modelo3.fragmentShader = noiseShader

rend.models.append(modelo3)


modelo1 = Model("barril/barril.obj")
modelo1.LoadTexture("barril/barril.bmp")
modelo1.translate[0] = -25
modelo1.translate[1] = -12
modelo1.translate[2] = -70

modelo1.rotate[0] = 0
modelo1.rotate[1] = 180
modelo1.rotate[2] = 180

modelo1.scale[0] = 5
modelo1.scale[1] = 5
modelo1.scale[2] = 5
modelo1.vertexShader = vertexShader
modelo1.fragmentShader = normalMappingShader

rend.models.append(modelo1)




modelo2 = Model("barril/barril.obj")
modelo2.LoadTexture("barril/barril.bmp")
modelo2.translate[0] = 25
modelo1.translate[1] = -12
modelo2.translate[2] = -50

modelo2.rotate[0] = 0
modelo2.rotate[1] = 180
modelo2.rotate[2] = 180

modelo2.scale[0] = 5
modelo2.scale[1] = 5
modelo2.scale[2] = 5
modelo2.vertexShader = vertexShader
modelo2.fragmentShader = fireShader

rend.models.append(modelo2)






isRunning = True
while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

            elif event.key == pygame.K_1:
                rend.primitiveType = POINTS

            elif event.key == pygame.K_2:
                rend.primitiveType = LINES

            elif event.key == pygame.K_3:
                rend.primitiveType = TRIANGLES

            elif event.key == pygame.K_RIGHT:
                rend.camera.translate[0] += 1
            elif event.key == pygame.K_LEFT:
                rend.camera.translate[0] -= 1
            elif event.key == pygame.K_UP:
                rend.camera.translate[1] += 1
            elif event.key == pygame.K_DOWN:
                rend.camera.translate[1] -= 1

    rend.glClear()
    rend.glRender()

    pygame.display.flip()
    clock.tick(60)

rend.glGenerateFrameBuffer("output.bmp")

pygame.quit()
