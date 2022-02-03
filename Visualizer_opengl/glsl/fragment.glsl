#version 330 core

// Interpolated values from the vertex shaders
out vec4 FragColor;
//out float gl_PointSize;
void main()
{
    FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);

}