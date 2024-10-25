vertex_shader = """
#version 450 core
layout(location=0) in vec3 position;
layout(location=1) in vec2 textCoords;
layout(location=2) in vec3 normals;
out vec2 outTextCoords;
out vec3 outNormals;
uniform mat4 modelMatrix;
uniform float time;

void main()
{
  gl_Position = modelMatrix * vec4(position + normals * sin(time)/10, 1.0);
  outTextCoords =  textCoords;
  outNormals = normals;
}
"""
fragmet_shader = """
#version 450 core
in vec2 outTextCoords;
in vec3 outNormals;
out vec4 fragColor;
uniform sampler2D tex;
void main()
{
  fragColor = texture(tex, outTextCoords);
}
"""

shader_plata = """
#version 450 core
in vec2 outTextCoords;
in vec3 outNormals;

out vec4 fragColor;

uniform sampler2D tex;
uniform vec3 lightPos;
uniform vec3 viewPos;
uniform vec3 silverColor;
uniform float shininess; 

void main()
{
    vec4 baseColor = texture(tex, outTextCoords);

    vec3 norm = normalize(outNormals);
    
    vec3 lightDir = normalize(lightPos - gl_FragCoord.xyz);

    vec3 viewDir = normalize(viewPos - gl_FragCoord.xyz);

    vec3 ambient = 0.1 * silverColor;

    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * silverColor;

    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(norm, halfwayDir), 0.0), shininess);
    vec3 specular = vec3(1.0) * spec;

    vec3 lighting = ambient + diffuse + specular;

    fragColor = vec4(lighting * baseColor.rgb, baseColor.a);
}


"""
