import glm
from numpy import array, float32
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


class Buffer(object):
    def __init__(self, data):

        self.vertBuffer = array(data, float32)

        self.VBO = glGenBuffers(1)

        self.VAO = glGenVertexArrays(1)

    def Render(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindVertexArray(self.VAO)

        glBufferData(GL_ARRAY_BUFFER,
                     self.vertBuffer.nbytes,
                     self.vertBuffer,
                     GL_STATIC_DRAW)
        glVertexAttribPointer(0,
                              3,
                              GL_FLOAT,
                              GL_FALSE,
                              4 * 8,
                              ctypes.c_void_p(0))

        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1,
                              2,
                              GL_FLOAT,
                              GL_FALSE,
                              4 * 8,
                              ctypes.c_void_p(4*3))

        glEnableVertexAttribArray(1)

        glVertexAttribPointer(2,
                              3,
                              GL_FLOAT,
                              GL_FALSE,
                              4 * 8,
                              ctypes.c_void_p(4*5))

        glEnableVertexAttribArray(2)

        glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertBuffer)/8))
