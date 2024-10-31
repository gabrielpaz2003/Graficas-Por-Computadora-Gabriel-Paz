import pygame
from pygame.locals import *
from gl import Renderer
from buffer import Buffer
from shaders import *
from model import Model

width = 600
height = 600

pygame.init()

screen = pygame.display.set_mode(
    (width, height), pygame.OPENGL | pygame.DOUBLEBUF)

clock = pygame.time.Clock()

renderer = Renderer(screen)

vshader = vertex_shader
fshader = fragment_shader

renderer.SetShaders(vshader, fshader)

madeModel = Model('models/razenade.obj')
madeModel.AddTextures('textures/razenade.bmp')
renderer.scene.append(madeModel)
madeModel.rotation.y = 180
madeModel.scale = (8, 8, 8)
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
            elif event.key == pygame.K_3:
                vshader = vertex_shader
                renderer.SetShaders(vshader, fshader)
            elif event.key == pygame.K_4:
                fshader = fragment_shader
                renderer.SetShaders(vshader, fshader)
            elif event.key == pygame.K_5:
                fshader = scrolling_texture_shader
                renderer.SetShaders(vshader, fshader)
            elif event.key == pygame.K_6:
                fshader = color_inversion_shader
                renderer.SetShaders(vshader, fshader)
            elif event.key == pygame.K_7:
                fshader = grayscale_shader
                renderer.SetShaders(vshader, fshader)
            elif event.key == pygame.K_8:
                vshader = explode_shader
                renderer.SetShaders(vshader, fshader)
            elif event.key == pygame.K_9:
                vshader = wobble_shader
                renderer.SetShaders(vshader, fshader) 
            elif event.key == pygame.K_0:
                vshader = rotation_shader
                renderer.SetShaders(vshader, fshader) 
    if keys[K_LEFT]:
        nadeModel.rotation.y -= 45 * deltaTime

    elif keys[K_RIGHT]:
        nadeModel.rotation.y += 45 * deltaTime

    renderer.time += deltaTime
    renderer.Render()
    pygame.display.flip()

pygame.quit()
