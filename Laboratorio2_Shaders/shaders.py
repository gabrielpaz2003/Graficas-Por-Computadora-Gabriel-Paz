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

    vt = MatrixVectorProduct(MatrixProduct(MatrixProduct(MatrixProduct(viewportMatrix, projectionMatrix), viewMatrix), modelMatrix), vt)

    vt = [vt[0] / vt[3],
          vt[1] / vt[3],
          vt[2] / vt[3]]

    return vt


def fragmentShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    textureList = kwargs["textureList"]
    dirLight = kwargs["dirLight"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]

    r = 1
    g = 1
    b = 1

    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    if len(textureList) > 0:
        texColor = textureList[0].getColor(vtP[0], vtP[1])
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]

    return [r, g, b]


def normalMappingShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    textureList = kwargs["textureList"]
    dirLight = kwargs["dirLight"]

    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]

    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2]]

    if len(textureList) > 1:
        tangentNormal = textureList[1].getColor(u, v)
        normal = [normal[0] + (tangentNormal[0] * 2 - 1),
                  normal[1] + (tangentNormal[1] * 2 - 1),
                  normal[2] + (tangentNormal[2] * 2 - 1)]

    normal = normalize(normal)

    intensity = max(0, sum([normal[i] * dirLight[i] for i in range(3)]))

    r, g, b = [intensity] * 3

    return [r, g, b]


def noiseShader(**kwargs):
    u, v, w = kwargs["bCoords"]

    noise = random.random()

    r = g = b = noise

    return [r, g, b]


def fireShader(**kwargs):
    u, v, w = kwargs["bCoords"]

    time = kwargs.get("time", 0)

    r = 1
    g = max(0, min(1, sin(time + u * 10) * 0.5 + 0.5 + v))
    b = max(0, min(1, sin(time + v * 10) * 0.5))

    return [r, g, b]
