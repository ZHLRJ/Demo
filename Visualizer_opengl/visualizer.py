# -*- coding: utf-8 -*-
'''
@Time    : 11/3/21 
@Author  : Zhang Haoliang
'''
import glfw
import OpenGL.GL as gl
import OpenGL.GLU as glu
import pylab
import glm
from Visualizer_opengl.utils.MVPControl import MVPControl
from Visualizer_opengl.utils.shaderLoader import Shader
import numpy as np
# other settings


#



def Render(vertices,triangles,Center_point=[],background_color=(0.9,0.9,0.9),SCR_WIDTH = 800,SCR_HEIGHT = 600,
           ):
    # Initialize the library
    if not glfw.init():
        return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.SAMPLES, 4)
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(SCR_WIDTH, SCR_HEIGHT, "Mesh Visualization", None, None)

    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)
    # gl.glDepthFunc(gl.GL_LESS)
    gl.glEnable(gl.GL_DEPTH_TEST)

    gl.glEnable(gl.GL_PROGRAM_POINT_SIZE)
    # gl.glEnable(gl.GL_CULL_FACE)
    # Load the vertices infomation form obj file
    # Read shader files
    shader = Shader()



    VAO = gl.glGenVertexArrays(1)  # pylint: disable=W0612
    gl.glBindVertexArray(VAO)
    # Do VBO
    vertexbuffer=gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER,vertexbuffer)
    gl.glBufferData(gl.GL_ARRAY_BUFFER,len(vertices)*len(vertices[0])*4,vertices,gl.GL_STATIC_DRAW)
    # # EBO buffer
    EBO=gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, EBO)
    gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, len(triangles) *len(triangles[0])*2,triangles, gl.GL_STATIC_DRAW)
    if not Center_point:
        Center_point=[i for i in range(len(vertices))]
    Center_point=np.array(Center_point,dtype=np.int16)

    PBO=gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, PBO)
    gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, len(Center_point)*2,Center_point, gl.GL_STATIC_DRAW)

    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 4*3, gl.ctypes.c_void_p(0))
    gl.glEnableVertexAttribArray(0)
    shader.initShaderFromGLSL(["glsl/vertex.glsl"], ["glsl/fragment.glsl"])
    MVP_ID = gl.glGetUniformLocation(shader.program, "MVP")
    Projection_ID=gl.glGetUniformLocation(shader.program, "projection")
    # Model = glm.mat4(1.0)
    controller = MVPControl(window,vertices)
    # controller.camerapose()
    # MVP_matrix_initial = calc_MVP(controller)
    gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
    radius=0.5
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)
    print(gl.glGetFloat(gl.GL_POINT_SIZE_RANGE))
    gl.glPointSize(3)

    # For Highlight Points
    MeshState=True
    while not glfw.window_should_close(window) and glfw.get_key(window,glfw.KEY_ESCAPE)!=glfw.PRESS :
        # Render here, using pyOpenGL
        # camX = glm.sin(glfw.get_time()) * radius
        # camZ = glm.cos(glfw.get_time()) * radius

        gl.glClearColor(background_color[0],background_color[1],background_color[2], 1.0)
        # gl.glClearColor(1,0,0,1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        shader.begin()

        controller.update()
        view = glm.lookAt(controller.cameraPos, controller.cameraPos + controller.cameraFront, controller.cameraUp)
        if (glfw.get_key(window,glfw.KEY_M)==glfw.PRESS):
            MeshState=not MeshState
            glfw.wait_events_timeout(0.1)
        if MeshState :
            gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, EBO)
            gl.glDrawElements(gl.GL_TRIANGLES, len(triangles) *len(triangles[0]), gl.GL_UNSIGNED_SHORT, None)

        else:
            # gl.glBindVertexArray(PBO)
            gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, PBO)
            gl.glDrawElements(gl.GL_POINTS,len(Center_point), gl.GL_UNSIGNED_SHORT, None)

        gl.glUniformMatrix4fv(MVP_ID, 1, gl.GL_FALSE, glm.value_ptr(view))
        gl.glUniformMatrix4fv(Projection_ID, 1, gl.GL_FALSE, glm.value_ptr(controller.projection))

        # gl.glDrawArrays(gl.GL_POINTS, 0, len(vertices)*len(vertices[0]))

        glfw.swap_buffers(window)
        glfw.poll_events()


    # glDeleteProgram(shader.program)
    gl.glDeleteProgram(shader.program)
    glfw.terminate()






