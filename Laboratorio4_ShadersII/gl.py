import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np


class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        # el color del fondo
        glClearColor(0.2, 0.2, 0.2, 1.0)

        # lo que prendo aqui es el z buffer
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)

        self.time = 0
        self.value = 0
        # no es tan facil de venir y agregar el triangulo . Sino que voy a crear una nueva clase para guardarlo

        self.scene = []
        self.active_shaders = None

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

    def Render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.active_shaders is not None:
            glUseProgram(self.active_shaders)

            time_location = glGetUniformLocation(self.active_shaders, "time")
            model_matrix_location = glGetUniformLocation(
                self.active_shaders, "modelMatrix")

            glUniform1f(time_location, self.time)

        last_model_matrix = None

        for obj in self.scene:
            if self.active_shaders is not None:
                current_model_matrix = obj.GetModelMatrix()

                if not np.array_equal(current_model_matrix, last_model_matrix):
                    last_model_matrix = current_model_matrix
                    glUniformMatrix4fv(
                        model_matrix_location, 1, GL_FALSE, glm.value_ptr(current_model_matrix))

            obj.Render()
