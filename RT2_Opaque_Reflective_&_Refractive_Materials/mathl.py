from math import cos, pi, sin, asin, acos


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
            cofactorRow.append(((-1) ** (r + c)) * minor.determinante())
        cofactors.append(cofactorRow)

    cofactorMatrix = cofactors
    cofactors_transposed = cofactorMatrix.transponer()

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


def normalize(arr):
    norm_value = norm(arr)
    return [a / norm_value for a in arr] if norm_value != 0 else arr


def suma(arr1: list, arr2: list):
    result = [a + b for a, b in zip(arr1, arr2)]

    return result


def resta(arr1: list, arr2: list):
    result = [a - b for a, b in zip(arr1, arr2)]

    return result


def producto(v1, v2, out=None, where=None):
    if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
        result = v1 * v2
    elif isinstance(v1, (int, float)) or isinstance(v2, (int, float)):
        scalar = v1 if isinstance(v1, (int, float)) else v2
        array = v1 if isinstance(v1, list) else v2
        result = [scalar * a for a in array]
    else:
        if len(v1) != len(v2):
            raise ValueError("Both arrays must have the same length")
        result = [a * b for a, b in zip(v1, v2)]

    if where is not None and isinstance(result, list):
        result = [r if w else o for r, o, w in zip(result, out, where)]

    if out is not None and isinstance(result, list):
        out[:] = result
        return out

    return result


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


def norm(arr: list) -> float:
    return (sum(a**2 for a in arr))**(1/2)


def reflectVector(normal, direction):
    reflect = 2 * dotProduct(normal, direction)
    reflect = producto(reflect, normal)
    reflect = resta(reflect, direction)
    reflect = [a / norm(reflect) for a in reflect]
    return reflect


def refractVector(normal, incident, n1, n2):
    c1 = dotProduct(normal, incident)

    if c1 < 0:
        c1 = -c1
    else:
        normal = [x * -1 for x in normal]
        n1, n2 = n2, n1

    n = n1 / n2

    temp = suma(incident, [c1 * x for x in normal])
    T = resta([n * x for x in temp], [normal[i] *
                                      ((1 - n**2 * (1 - c1**2)) ** 0.5) for i in range(len(normal))])

    norm_T = norm(T)
    return [x / norm_T for x in T]


def totalInternalReflection(normal, incident, n1, n2):
    c1 = dotProduct(normal, incident)
    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1

    if n1 < n2:
        return False

    theta1 = acos(c1)
    thetaC = asin(n2 / n1)

    return theta1 >= thetaC


def fresnel(normal, incident, n1, n2):
    c1 = dotProduct(normal, incident)
    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1

    s2 = (n1 * (1 - c1**2) ** 0.5) / n2
    c2 = (1 - s2 ** 2) ** 0.5

    F1 = (((n2 * c1) - (n1 * c2)) / ((n2 * c1) + (n1 * c2))) ** 2
    F2 = (((n1 * c2) - (n2 * c1)) / ((n1 * c2) + (n2 * c1))) ** 2

    Kr = (F1 + F2) / 2
    Kt = 1 - Kr
    return Kr, Kt
