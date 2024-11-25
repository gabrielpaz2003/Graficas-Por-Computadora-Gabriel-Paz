import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from camera import *
from skybox import Skybox


class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        glClearColor(0.2, 0.2, 0.2, 1.0)
        glEnable(GL_DEPTH_TEST)

        glViewport(0, 0, self.width, self.height)

        self.camera = Camera(self.width, self.height)

        self.time = 0
        self.value = 0

        self.mouse_x = 0
        self.mouse_y = 0

        self.scene = []
        self.active_shaders = None

        self.skybox = None

    def CreateSkybox(self, textureList, vShader, fShader):
        self.skybox = Skybox(textureList, vShader, fShader)

    def FillMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def WireFrameMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def SetShaders(self, vShader, fShader):
        if vShader is not None and fShader is not None:
            self.active_shaders = compileProgram(compileShader(vShader, GL_VERTEX_SHADER),
                                                 compileShader(fShader, GL_FRAGMENT_SHADER))
        else:
            self.active_shaders = None

    def SetMousePos(self, mouse_x, mouse_y):
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y

    def Render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.skybox is not None:
            self.skybox.Render(self.camera.GetViewMatrix(),
                               self.camera.GetProjectionMatrix())

        if self.active_shaders is not None:
            current_view_matrix = self.camera.GetViewMatrix()
            current_projection_matrix = self.camera.GetProjectionMatrix()
            glUseProgram(self.active_shaders)
            glUniform1f(glGetUniformLocation(
                self.active_shaders, "time"), self.time)
            glUniformMatrix4fv(glGetUniformLocation(self.active_shaders, "viewMatrix"),
                               1, GL_FALSE, glm.value_ptr(current_view_matrix))
            glUniformMatrix4fv(glGetUniformLocation(self.active_shaders, "projectionMatrix"),
                               1, GL_FALSE, glm.value_ptr(current_projection_matrix))

            normalized_x, normalized_y = self.normalize_mouse_position()
            glUniform1f(glGetUniformLocation(
                self.active_shaders, "mouse_x"), normalized_x)
            glUniform1f(glGetUniformLocation(
                self.active_shaders, "mouse_y"), normalized_y)

        for obj in self.scene:
            if self.active_shaders is not None:
                current_model_matrix = obj.GetModelMatrix()
                glUniformMatrix4fv(glGetUniformLocation(self.active_shaders, "modelMatrix"),
                                   1, GL_FALSE, glm.value_ptr(current_model_matrix))
            obj.Render()

    def normalize_mouse_position(self):
        ndc_x = (2.0 * self.mouse_x / self.width) - 1.0
        ndc_y = (1.0 - (2.0 * self.mouse_y / self.height))
        return ndc_x, ndc_y
