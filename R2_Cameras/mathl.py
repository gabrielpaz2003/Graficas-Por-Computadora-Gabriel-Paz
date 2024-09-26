from math import cos, pi, sin


def MatrixProduct(A, B):
    result = [[x * 0 for x in range(len(A[0]))] for i in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result


def MatrixVectorProduct(A, v):
    result = [0] * len(A)

    for i in range(len(A)):
        for j in range(len(A[0])):
            result[i] += A[i][j] * v[j]

    return result


def getMinor(mat, i, j):
    return [row[:j] + row[j + 1:] for row in (mat[:i] + mat[i + 1:])]


def determinante(mat):
    if len(mat) == 2:
        return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]

    det = 0

    for i in range(len(mat)):
        det += ((-1) ** i) * mat[0][i] * \
            determinante(getMinor(mat, 0, i))
    return det


def transponer(A):
    mat = A
    return [list(row) for row in zip(*mat)]


def inverse(mat):
    det = determinante(mat)

    n = len(mat)

    if n == 2:
        return [[mat[1][1] / det, -1 * mat[0][1] / det],
                [-1 * mat[1][0] / det, mat[0][0] / det]]

    cofactors = []
    for r in range(n):
        cofactorRow = []
        for c in range(n):
            minor = getMinor(mat, r, c)
            cofactorRow.append(((-1) ** (r + c)) * determinante(minor))
        cofactors.append(cofactorRow)

    cofactorMatrix = cofactors
    cofactors_transposed = transponer(cofactorMatrix)

    inverse_matrix = []
    for r in range(n):
        row = [value / det for value in cofactors_transposed[r]]
        inverse_matrix.append(row)

    return inverse_matrix


def TranslationMatrix(x, y, z):
    return [[1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1],
            ]


def ScaleMatrix(x, y, z):
    return [[x, 0, 0, 0],
            [0, y, 0, 0],
            [0, 0, z, 0],
            [0, 0, 0, 1],
            ]


def RotationMatrix(pitch, yaw, roll):
    pitch *= pi / 180
    yaw *= pi / 180
    roll *= pi / 180

    pitchMat = [
        [1, 0, 0, 0],
        [0, cos(pitch), -sin(pitch), 0],
        [0, sin(pitch), cos(pitch), 0],
        [0, 0, 0, 1],
    ]

    yawMat = [
        [cos(yaw), 0, sin(yaw), 0],
        [0, 1, 0, 0],
        [-sin(yaw), 0, cos(yaw), 0],
        [0, 0, 0, 1],
    ]

    rollMat = [
        [cos(roll), -sin(roll), 0, 0],
        [sin(roll), cos(roll), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]

    return MatrixProduct(MatrixProduct(pitchMat, yawMat), rollMat)


def dotProduct(v1, v2):
    return sum(a*b for a, b in zip(v1, v2))


def norm(arr: list) -> float:
    return (sum(a**2 for a in arr))**(1/2)


def normalize(v):
    length = (sum(a*a for a in v))**(0.5)
    return [a / length for a in v]


def reflect(lightDir, normal):
    dotLN = dotProduct(lightDir, normal)
    return [2 * dotLN * n - l for n, l in zip(normal, lightDir)]


def barycentricCoords(A, B, C, P):

    areaPCB = abs((P[0]*C[1] + C[0]*B[1] + B[0]*P[1]) -
                  (P[1]*C[0] + C[1]*B[0] + B[1]*P[0]))

    areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) -
                  (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))

    areaABP = abs((A[0]*B[1] + B[0]*P[1] + P[0]*A[1]) -
                  (A[1]*B[0] + B[1]*P[0] + P[1]*A[0]))

    areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) -
                  (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))

    if areaABC == 0:
        return None

    u = areaPCB / areaABC
    v = areaACP / areaABC
    w = areaABP / areaABC

    if 0 <= u <= 1 and 0 <= v <= 1 and 0 <= w <= 1:
        return (u, v, w)
    else:
        return None
