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

skyboxTextures = ["right.jpg",
                  "left.jpg",
                  "top.jpg",
                  "bottom.jpg",
                  "front.jpg",
                  "back.jpg"]

vshader = vertex_shader
fshader = fragment_shader

renderer.CreateSkybox(skyboxTextures, skybox_vertex_shader,
                      skybox_fragment_shader)

camDistance = 20
camAngle = 0
camPitch = 0

isDragging = False
lastMouseX = 0
lastMouseY = 0

renderer.SetShaders(vshader, fshader)

model = 'models/model.obj'
texture = 'textures/model.bmp'

nadeModel = Model(model)
nadeModel.AddTextures(texture)
renderer.scene.append(nadeModel)
nadeModel.rotation.y = 0
nadeModel.scale = (10, 10, 10)
nadeModel.translation.z = -4

isRunning = True

y_limit = 3.0

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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                isDragging = True
                lastMouseX, lastMouseY = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                isDragging = False

        elif event.type == pygame.MOUSEMOTION:
            if isDragging:
                mouseX, mouseY = event.pos
                deltaX = mouseX - lastMouseX
                deltaY = mouseY - lastMouseY
                lastMouseX, lastMouseY = mouseX, mouseY

                sensitivity = 0.2
                camAngle += deltaX * sensitivity
                camPitch += deltaY * sensitivity

                camPitch = max(-89.0, min(89.0, camPitch))

    if keys[K_s]:
        camDistance -= 2 * deltaTime
    elif keys[K_w]:
        camDistance += 2 * deltaTime

    if keys[K_UP]:
        renderer.camera.usingOrbit = False
        renderer.camera.position.y = min(
            renderer.camera.position.y + 0.1, y_limit)
    elif keys[K_DOWN]:
        renderer.camera.usingOrbit = False
        renderer.camera.position.y = max(
            renderer.camera.position.y - 0.1, -y_limit)


    renderer.time += deltaTime

    if renderer.camera.usingOrbit:
        renderer.camera.Orbit(nadeModel.translation,
                              camDistance, camAngle, camPitch)
    else:
        renderer.camera.LookAt(nadeModel.translation)
    renderer.Render()
    pygame.display.flip()

pygame.quit()
