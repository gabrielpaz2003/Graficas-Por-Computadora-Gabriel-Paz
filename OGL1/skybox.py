
from numpy import array, float32
import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pygame


class Skybox(object):
    def __init__(self, textureList, vertexShader, fragmentShader):

        skyboxVertices = [-1.0,  1.0, -1.0,
                          -1.0, -1.0, -1.0,
                          1.0, -1.0, -1.0,
                          1.0, -1.0, -1.0,
                          1.0,  1.0, -1.0,
                          -1.0,  1.0, -1.0,

                          -1.0, -1.0,  1.0,
                          -1.0, -1.0, -1.0,
                          -1.0,  1.0, -1.0,
                          -1.0,  1.0, -1.0,
                          -1.0,  1.0,  1.0,
                          -1.0, -1.0,  1.0,

                          1.0, -1.0, -1.0,
                          1.0, -1.0,  1.0,
                          1.0,  1.0,  1.0,
                          1.0,  1.0,  1.0,
                          1.0,  1.0, -1.0,
                          1.0, -1.0, -1.0,

                          -1.0, -1.0,  1.0,
                          -1.0,  1.0,  1.0,
                          1.0,  1.0,  1.0,
                          1.0,  1.0,  1.0,
                          1.0, -1.0,  1.0,
                          -1.0, -1.0,  1.0,

                          -1.0,  1.0, -1.0,
                          1.0,  1.0, -1.0,
                          1.0,  1.0,  1.0,
                          1.0,  1.0,  1.0,
                          -1.0,  1.0,  1.0,
                          -1.0,  1.0, -1.0,

                          -1.0, -1.0, -1.0,
                          -1.0, -1.0,  1.0,
                          1.0, -1.0, -1.0,
                          1.0, -1.0, -1.0,
                          -1.0, -1.0,  1.0,
                          1.0, -1.0,  1.0]

        self.vertexBuffer = array(skyboxVertices, dtype=float32)
        self.VBO = glGenBuffers(1)
        self.VAO = glGenVertexArrays(1)

        self.shaders = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER),
                                      compileShader(fragmentShader, GL_FRAGMENT_SHADER))

        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture)

        for i in range(len(textureList)):
            texture = pygame.image.load(textureList[i])
            textureData = pygame.image.tostring(texture, "RGB", False)

            glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i,
                         0,
                         GL_RGB,
                         texture.get_width(),
                         texture.get_height(),
                         0,
                         GL_RGB,
                         GL_UNSIGNED_BYTE,
                         textureData)

        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP,
                        GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP,
                        GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP,
                        GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)

    def Render(self, viewMatrix, projectionMatrix):
        if self.shaders == None:
            return

        glUseProgram(self.shaders)

        viewMatrix = glm.mat4(glm.mat3(viewMatrix))

        glUniformMatrix4fv(glGetUniformLocation(self.shaders, "viewMatrix"),
                           1, GL_FALSE, glm.value_ptr(viewMatrix))

        glUniformMatrix4fv(glGetUniformLocation(self.shaders, "projectionMatrix"),
                           1, GL_FALSE, glm.value_ptr(projectionMatrix))

        glDepthMask(GL_FALSE)

        glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindVertexArray(self.VAO)

        glBufferData(GL_ARRAY_BUFFER,
                     self.vertexBuffer.nbytes,
                     self.vertexBuffer,
                     GL_STATIC_DRAW)

        glVertexAttribPointer(0,
                              3,
                              GL_FLOAT,
                              GL_FALSE,
                              4 * 3,
                              ctypes.c_void_p(0))

        glEnableVertexAttribArray(0)

        glDrawArrays(GL_TRIANGLES, 0, 36)

        glDepthMask(GL_TRUE)
