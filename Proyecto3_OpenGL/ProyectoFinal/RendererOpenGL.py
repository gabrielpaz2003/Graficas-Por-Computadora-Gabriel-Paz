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

camDistance = 50
camAngle = 0
camPitch = 0

isDragging = False
lastMouseX = 0
lastMouseY = 0

renderer.SetShaders(vshader, fshader)

model_index = 0

duck = Model('models/duck.obj')
duck.AddTextures('textures/duck.bmp')
renderer.scene.append(duck)
duck.rotation.x = 90
duck.rotation.y = 180
duck.rotation.z = -90
duck.scale = (0.1, 0.1, 0.2)
duck.translation.x = 10
duck.translation.y = -19
duck.translation.z = -15

gato = Model('models/cat.obj')
gato.AddTextures('textures/cat.bmp')
renderer.scene.append(gato)
gato.rotation.x = 90
gato.rotation.y = 180
gato.rotation.z = -90
gato.scale = (0.1, 0.1, 0.1)
gato.translation.x = 20
gato.translation.y = -19
gato.translation.z = -5

road = Model('models/road.obj')
road.AddTextures('textures/road.bmp')
renderer.scene.append(road)
road.rotation.x = 0
road.rotation.y = 90
road.rotation.z = 0
road.scale = (7, 7, 7)
road.translation.x = 0
road.translation.y = -20
road.translation.z = -6

lobo = Model('models/wolf.obj')
lobo.AddTextures('textures/wolf.bmp')
renderer.scene.append(lobo)
lobo.rotation.x = 0
lobo.rotation.y = 90
lobo.rotation.z = 0
lobo.scale = (15, 15, 15)
lobo.translation.x = -15
lobo.translation.y = -18
lobo.translation.z = -3
isRunning = True

y_limit = 3.0


def update_lookat_target():
    current_model = renderer.scene[model_index]
    renderer.camera.LookAt(current_model.translation)

music = pygame.mixer.music.load('musica.mp3')
pygame.mixer.music.play(-1)


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
            elif event.button == 3:
                model_index = (model_index + 1) % len(renderer.scene)
                update_lookat_target()
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
        renderer.camera.Orbit(renderer.scene[model_index].translation,
                              camDistance, camAngle, camPitch)
    else:
        renderer.camera.LookAt(renderer.scene[model_index].translation)

    renderer.Render()
    pygame.display.flip()

pygame.quit()
