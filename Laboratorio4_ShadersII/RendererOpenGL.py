import pygame
from pygame.locals import *
from gl import Renderer
from buffer import Buffer
from shaders import *
from model import Model

width = 960
height = 540

pygame.init()

screen = pygame.display.set_mode(
    (width, height), pygame.OPENGL | pygame.DOUBLEBUF)

clock = pygame.time.Clock()

renderer = Renderer(screen=screen)

renderer.SetShaders(vShader=vertex_shader, fShader=fragmet_shader)

faceModel = Model('face.obj')
faceModel.AddTextures('model.bmp')
renderer.scene.append(faceModel)
faceModel.rotation.y = 180
isRunning = True

while isRunning:
    deltaTime = clock.tick(60) / 1000
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            elif event.key == pygame.K_1:
                renderer.FillMode()
            elif event.key == pygame.K_2:
                renderer.WireFrameMode()

    if keys[K_LEFT]:
        faceModel.rotation.y -= 10*deltaTime
    elif keys[K_RIGHT]:
        faceModel.rotation.y += 10*deltaTime

    renderer.time += deltaTime
    renderer.Render()
    pygame.display.flip()

pygame.quit()
