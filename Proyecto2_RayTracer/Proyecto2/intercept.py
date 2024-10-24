class Intercept(object):
    def __init__(self, point, normal, rayDirection, distance, texCoords, obj):
        self.point = point
        self.normal = normal
        self.distance = distance
        self.texCoords = texCoords
        self.rayDirection = rayDirection
        self.obj = obj

