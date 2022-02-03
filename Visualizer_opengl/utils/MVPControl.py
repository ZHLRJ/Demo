
import glfw
import glm
import numpy as np
def Boundary(objpoints):
    x,y,z=objpoints[:,0],objpoints[:,1],objpoints[:,2]
    # print([x.min(),x.max()],[y.min(),y.max()],[z.min(),z.max()],"The mean",np.mean(objpoints,axis=0))
    return [x.min(),x.max()],[y.min(),y.max()],[z.min(),z.max()]

class MVPControl:

    def __init__(self,window,vertices,cameraSpeed=0.008,*args,**kwargs):
        self.Xboundary, self.Yboundary, self.Zboundary = Boundary(vertices)
        print(self.Xboundary, self.Yboundary, self.Zboundary)
        self.meanpoint=np.mean(vertices,axis=0)

        self.cameraSpeed = cameraSpeed
        self.cameraFront=glm.vec3(0,0,-1)
        self.cameraUp=glm.vec3(0.0, 1.0, 0.0)
        self.cameraPos=glm.vec3(self.meanpoint[0],self.meanpoint[1],self.meanpoint[2]+0.5)
        self.window=window
        self.Mousepress=False
        self.yaw=-90
        self.pitch=0
        self.lastX=800/2
        self.lastY=600/2
        self.fov=100

        self.projection = glm.perspective(glm.radians(self.fov), 8 / 6, -1, 1)
    def glfw_mouse_button_callback(self, window, button, action, mods):
        """Handle mouse button events and forward them to the example

        Args:
            window: The window
            button: The button creating the event
            action: Button action (press or release)
            mods: They modifiers such as ctrl or shift
        """
        # self._handle_modifiers(mods)
        # button = self._mouse_button_map.get(button, None)
        if button is None:
            return

        if action == glfw.PRESS:
            self.lastX, self.lastY = glfw.get_cursor_pos(self.window)
            self.Mousepress=True
            # print("Mouse click")
        else:
            self.Mousepress = False
            # print("Mouse release +++=")


    def mouse_callback(self):
        glfw.set_mouse_button_callback(self.window,self.glfw_mouse_button_callback)
        # self.detecclick()
        if self.Mousepress:

            xpos, ypos = glfw.get_cursor_pos(self.window)
            # print("Mouse move ")
            xoffset = xpos - self.lastX
            yoffset = self.lastY - ypos
            self.lastX = xpos
            self.lastY = ypos

            sensitivity = 0.5

            xoffset *= sensitivity
            yoffset *= sensitivity

            self.yaw += xoffset
            self.pitch += yoffset

            if (self.pitch > 89.0):
                self.pitch = 89.0
            if (self.pitch < -89.0):
                self.pitch = -89.0

            direction = glm.vec3(glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch)),
                                 glm.sin(glm.radians(
                                     self.pitch)),
                                 glm.sin(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch)))
            self.cameraFront = glm.normalize(direction)

    def scroll_callback(self, window, xoffset,yoffset):

        self.fov -= yoffset
        # print(self.fov)
        if  self.fov < 1.0:
            self.fov = 1.0
        if  self.fov > 45.0:
            self.fov = 45.0


    def scroll(self):
        glfw.set_scroll_callback(self.window, self.scroll_callback)
        self.projection = glm.perspective(glm.radians(self.fov), 800 / 600, 0.01, 60.0)
        # self.cameraPos*=self.projection
    def camerapose(self):

        if (glfw.get_key(self.window,glfw.KEY_W)==glfw.PRESS):
            self.cameraPos += self.cameraSpeed * self.cameraFront
            # print(self.cameraPos)
        if (glfw.get_key(self.window,glfw.KEY_S)==glfw.PRESS):
            self.cameraPos -= self.cameraSpeed * self.cameraFront
        if (glfw.get_key(self.window,glfw.KEY_A)==glfw.PRESS):
            self.cameraPos -= glm.normalize(glm.cross(self.cameraFront, self.cameraUp)) * self.cameraSpeed
        if (glfw.get_key(self.window, glfw.KEY_D) == glfw.PRESS):
            self.cameraPos += glm.normalize(glm.cross(self.cameraFront, self.cameraUp)) * self.cameraSpeed
        if (glfw.get_key(self.window,glfw.KEY_R)==glfw.PRESS):
            self.cameraFront = glm.vec3(0, 0, -1)
            self.cameraUp = glm.vec3(0.0, 1.0, 0.0)
            self.cameraPos=glm.vec3(self.meanpoint[0],self.meanpoint[1],self.meanpoint[2]+0.5)

    def update(self):
        self.camerapose()
        self.mouse_callback()
        self.scroll()