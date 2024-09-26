from math import sin, cos, pi
from mathl import dotProduct, normalize, MatrixProduct, MatrixVectorProduct
import random


def vertexShader(vertex, **kwargs):
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    viewportMatrix = kwargs["viewportMatrix"]

    vt = [vertex[0],
          vertex[1],
          vertex[2],
          1]

    vt = MatrixVectorProduct(MatrixProduct(MatrixProduct(MatrixProduct(
        viewportMatrix, projectionMatrix), viewMatrix), modelMatrix), vt)

    vt = [vt[0] / vt[3],
          vt[1] / vt[3],
          vt[2] / vt[3]]

    return vt


def fragmentShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    r = 1
    g = 1
    b = 1

    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]

    return [r, g, b]
