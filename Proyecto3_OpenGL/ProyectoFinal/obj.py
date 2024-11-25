import re


class Obj(object):
    def __init__(self, filename):
        with open(filename, "r") as file:
            lines = file.read().splitlines()
        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []
        for line in lines:
            line = line.rstrip()

            try:
                prefix, value = line.split(' ', 1)

            except:
                continue

            if prefix == 'v':
                vertice = list(map(float, filter(None, value.split(' '))))
                self.vertices.append(vertice)

            elif prefix == 'vt':
                vts = list(map(float, filter(None, value.split(' '))))
                self.texcoords.append([vts[0], vts[1]])

            elif prefix == 'vn':
                norm = list(map(float, filter(None, value.split(' '))))
                self.normals.append(norm)

            elif prefix == 'f':
                self.faces.append(
                    [list(map(int, filter(None, re.split(r'/|//', face)))) for face in value.split(' ')])
