from math import sin, cos, pi
from mathl import dotProduct, normalize, MatrixProduct, MatrixVectorProduct
import random


def vertexShader(vertex, **kwargs):
    modelMatrix = kwargs["modelMatrix"]


    vt = [vertex[0],
          vertex[1],
          vertex[2],
          1]

    vt = MatrixVectorProduct(modelMatrix, vt)

    vt = [vt[0] / vt[3],
          vt[1] / vt[3],
          vt[2] / vt[3]]

    return vt

