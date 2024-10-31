
distortion_noise_shader = """
#version 450 core
in vec3 position;
in vec2 textCoords;
in vec3 normals;
out vec2 outTextCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform mat4 modelMatrix;
uniform float time;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

float noise(vec3 p)
{
    // Simplex or Perlin noise function implementation
    // For the sake of example, let's use a placeholder
    return fract(sin(dot(p, vec3(12.9898,78.233,45.164))) * 43758.5453);
}

void main()
{
  float displacement = noise(position + time);
  vec3 newPosition = position + normals * displacement * 0.1;
  outPosition = modelMatrix * vec4(newPosition, 1.0);
  gl_Position = projectionMatrix * viewMatrix * outPosition;
  outTextCoords = textCoords;
  outNormals = normals;
}
"""
color_inversion_shader = """
#version 450 core
in vec2 outTextCoords;

out vec4 fragColor;
uniform sampler2D tex;

void main()
{
  vec4 color = texture(tex, outTextCoords);
  fragColor = vec4(1.0 - color.rgb, color.a);
}
"""
grayscale_shader = """
#version 450 core
in vec2 outTextCoords;
in vec3 outNormals;

out vec4 fragColor;
uniform sampler2D tex;

void main()
{
  vec4 color = texture(tex, outTextCoords);
  float gray = dot(color.rgb, vec3(0.299, 0.587, 0.114));
  fragColor = vec4(vec3(gray), color.a);
}
"""



scrolling_texture_shader = """
#version 450 core
in vec2 outTextCoords;
in vec3 outNormals;

out vec4 fragColor;
uniform sampler2D tex;
uniform float time;

void main()
{
  vec2 scrolledCoords = outTextCoords + vec2(time * 0.1, 0.0);
  fragColor = texture(tex, scrolledCoords);
}
"""


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
  gl_Position = modelMatrix * vec4(position, 1.0);
  outTextCoords =  textCoords;
  outNormals = normals;
}
"""

fragment_shader = """
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




spin_vertex_shader = """
#version 450 core
layout(location=0) in vec3 position;
layout(location=1) in vec2 textCoords;
layout(location=2) in vec3 normals;

out vec2 outTextCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;
uniform vec3 rotationAxis; // Axis to rotate around (e.g., vec3(0.0, 1.0, 0.0) for Y-axis)

void main()
{
  // Normalize the rotation axis
  vec3 axis = normalize(rotationAxis);
  float angle = time; // Adjust rotation speed as needed

  // Calculate rotation matrix components
  float cosA = cos(angle);
  float sinA = sin(angle);
  float oneMinusCosA = 1.0 - cosA;

  // Build the rotation matrix
  mat3 rotationMatrix;
  rotationMatrix[0][0] = cosA + axis.x * axis.x * oneMinusCosA;
  rotationMatrix[0][1] = axis.x * axis.y * oneMinusCosA - axis.z * sinA;
  rotationMatrix[0][2] = axis.x * axis.z * oneMinusCosA + axis.y * sinA;

  rotationMatrix[1][0] = axis.y * axis.x * oneMinusCosA + axis.z * sinA;
  rotationMatrix[1][1] = cosA + axis.y * axis.y * oneMinusCosA;
  rotationMatrix[1][2] = axis.y * axis.z * oneMinusCosA - axis.x * sinA;

  rotationMatrix[2][0] = axis.z * axis.x * oneMinusCosA - axis.y * sinA;
  rotationMatrix[2][1] = axis.z * axis.y * oneMinusCosA + axis.x * sinA;
  rotationMatrix[2][2] = cosA + axis.z * axis.z * oneMinusCosA;

  // Apply rotation to position and normals
  vec3 rotatedPosition = rotationMatrix * position;
  vec3 rotatedNormal = rotationMatrix * normals;

  outPosition = modelMatrix * vec4(rotatedPosition, 1.0);
  gl_Position = projectionMatrix * viewMatrix * outPosition;
  outTextCoords = textCoords;
  outNormals = normalize(rotatedNormal);
}
"""
explode_shader = """
#version 450 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 textCoords;
layout(location = 2) in vec3 normals;

out vec2 outTextCoords;
out vec3 outNormals;

uniform mat4 modelMatrix;
uniform float time;

void main()
{
    float explosionFactor = abs(sin(time)) * 0.01;

    vec3 explodedPosition = position + normalize(position) * explosionFactor;

    gl_Position = modelMatrix * vec4(explodedPosition, 1.0);

    outTextCoords = textCoords;
    outNormals = normals;
}
"""

wobble_shader = """
#version 450 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 textCoords;
layout(location = 2) in vec3 normals;

out vec2 outTextCoords;
out vec3 outNormals;

uniform mat4 modelMatrix;
uniform float time;

void main()
{
    // Wobble factor based on position and time
    float wobbleFactor = sin(position.y * 10.0 + time * 5.0) * 0.02;

    // Displace the vertex position along its normal
    vec3 wobblePosition = position + normals * wobbleFactor;

    gl_Position = modelMatrix * vec4(wobblePosition, 1.0);

    outTextCoords = textCoords;
    outNormals = normals;
}
"""

rotation_shader = """
#version 450 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 textCoords;
layout(location = 2) in vec3 normals;

out vec2 outTextCoords;
out vec3 outNormals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;

void main()
{
    // Rotation parameters
    float rotationSpeed = 1.0; // Adjust this value to control rotation speed

    // Calculate the rotation angle based on time
    float angle = time * rotationSpeed;

    // Create the rotation matrix around the Y-axis
    mat4 rotationMatrix = mat4(
        cos(angle),  0.0, sin(angle), 0.0,
        0.0,         1.0, 0.0,        0.0,
       -sin(angle),  0.0, cos(angle), 0.0,
        0.0,         0.0, 0.0,        1.0
    );

    // Apply the rotation to the vertex position
    vec4 rotatedPosition = rotationMatrix * vec4(position, 1.0);

    // Transform the position to clip space
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * rotatedPosition;

    // Transform the normals
    mat3 normalMatrix = mat3(rotationMatrix);
    outNormals = normalize(normalMatrix * normals);

    // Pass through the texture coordinates
    outTextCoords = textCoords;
}
"""



edge_shader = """
#version 450 core

in vec2 outTextCoords;
out vec4 fragColor;

uniform sampler2D tex;
uniform vec2 texResolution; // Resolution of the texture

void main()
{
    float offset = 1.0 / texResolution.x; // Offset for Sobel operator

    vec3 horizEdge = vec3(
        -1.0 * texture(tex, outTextCoords + vec2(-offset, offset)).rgb +
        -2.0 * texture(tex, outTextCoords + vec2(-offset, 0.0)).rgb +
        -1.0 * texture(tex, outTextCoords + vec2(-offset, -offset)).rgb +
         1.0 * texture(tex, outTextCoords + vec2(offset, offset)).rgb +
         2.0 * texture(tex, outTextCoords + vec2(offset, 0.0)).rgb +
         1.0 * texture(tex, outTextCoords + vec2(offset, -offset)).rgb
    );

    vec3 vertEdge = vec3(
        1.0 * texture(tex, outTextCoords + vec2(-offset, offset)).rgb +
        2.0 * texture(tex, outTextCoords + vec2(0.0, offset)).rgb +
        1.0 * texture(tex, outTextCoords + vec2(offset, offset)).rgb +
       -1.0 * texture(tex, outTextCoords + vec2(-offset, -offset)).rgb +
       -2.0 * texture(tex, outTextCoords + vec2(0.0, -offset)).rgb +
       -1.0 * texture(tex, outTextCoords + vec2(offset, -offset)).rgb
    );

    vec3 edge = sqrt(horizEdge * horizEdge + vertEdge * vertEdge);

    fragColor = vec4(edge, 1.0);
}
"""

sun_shader = """
#version 450 core

in vec2 outTextCoords;
out vec4 fragColor;

uniform vec2 sunCenter;
uniform vec3 sunColor;
uniform float radius = 1.0;
uniform sampler2D tex;

void main()
{
    vec2 uv = outTextCoords - sunCenter;
    float dist = length(uv);

    float glowFactor = smoothstep(radius, radius * 0.5, dist);

    vec3 texColor = texture(tex, outTextCoords).rgb;
    vec3 finalColor = mix(sunColor, texColor, glowFactor);

    fragColor = vec4(finalColor, 1.0);
}
"""

sepia_shader = """
#version 450 core

in vec2 outTextCoords;
out vec4 fragColor;

uniform sampler2D tex;

void main()
{
    vec3 color = texture(tex, outTextCoords).rgb;
    vec3 sepia = vec3(
        dot(color, vec3(0.393, 0.769, 0.189)),
        dot(color, vec3(0.349, 0.686, 0.168)),
        dot(color, vec3(0.272, 0.534, 0.131))
    );

    fragColor = vec4(sepia, 1.0);
}


"""
