#version 330 core

// Input vertex data, different for all executions of this shader.
layout (location = 0) in vec3 aPos;
uniform mat4 MVP;
uniform mat4 projection;
void main()
{
    gl_Position =MVP *vec4(aPos, 1.0);

}