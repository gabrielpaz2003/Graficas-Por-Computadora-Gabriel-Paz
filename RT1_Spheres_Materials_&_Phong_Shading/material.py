class Material(object):
    def __init__(self, diffuse, spec=1.0, Ks=0.0):
        self.diffuse = diffuse
        self.spec = spec
        self.Ks = Ks

    def GetSurfaceColor(self, intercept, renderer):
        # Phong reflection model
        # LightColor = LightColors + Specular
        # FinalColor = DiffuseColor * LightColor
        lightColor = [0, 0, 0]
        finalColor = self.diffuse

        for light in renderer.lights:
            shadowIntercept = None
            if light.type == "Directional":
                lightDir = [(i * -1) for i in light.direction]
                shadowIntercept = renderer.glCastRay(
                    intercept.point, lightDir, intercept.obj)

            if shadowIntercept is None:
                currentLightColor = light.GetLightColor(intercept)
                currentSpecularColor = light.GetSpecularColor(
                    intercept, renderer.camera.translate)
                lightColor = [(lightColor[i] + currentLightColor[i] +
                               currentSpecularColor[i]) for i in range(3)]

        finalColor = [(finalColor[i] * lightColor[i]) for i in range(3)]
        finalColor = [min(1, finalColor[i]) for i in range(3)]
        return finalColor
