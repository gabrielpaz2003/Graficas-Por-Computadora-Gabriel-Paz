class Obj(object):
    def __init__(self, filename):

        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []

        try:
            with open(filename, "r", encoding="utf-8") as file:  # Specify UTF-8 encoding
                lines = file.read().splitlines()

            for line in lines:
                line = line.rstrip()

                try:
                    prefix, value = line.split(" ", 1)
                except ValueError:
                    continue
                if prefix == "v":  # Vértices
                    try:
                        vert = list(map(float, value.split()))
                        self.vertices.append(vert)
                    except ValueError:
                        print(
                            "Advertencia: Se encontro un vertice con valores no numericos.")
                elif prefix == "vt":
                    try:
                        vts = list(map(float, value.split()))
                        self.texcoords.append([vts[0], vts[1]])
                    except ValueError:
                        print(
                            "Advertencia: Se encontro una coordenada de textura con valores no numericos.")
                elif prefix == "vn":
                    try:
                        norm = list(map(float, value.split()))
                        self.normals.append(norm)
                    except ValueError:
                        print(
                            "Advertencia: Se encontro una normal con valores no numericos.")
                elif prefix == "f":
                    try:
                        face = []
                        verts = value.split()
                        for vert in verts:
                            vert = list(map(int, vert.split("/")))
                            face.append(vert)
                        self.faces.append(face)
                    except ValueError:
                        print(
                            "Advertencia: Se encontro una cara con indices no numericos.")
        except FileNotFoundError:
            print(f"Error: El archivo {filename} no se encontro.")
        except Exception as e:
            print(f"Error inesperado: {e}")

