#!/usr/bin/env python3
import sys

from glfw.GLFW import *
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

global arraySize
global arr

class Egg:
    def __init__(self, size):
        self.array = np.zeros((size,size,3))
        global arraySize
        arraySize = size

    def fill_array(self):
        u = [i/(arraySize) for i in range(arraySize)]
        v = [i/(arraySize) for i in range(arraySize)]
        
        for i in range(0,arraySize):
            for j in range(0,arraySize):
                self.array[i][j][0] = (-90 * u[i]**5 + 225 * u[i]**4 - 270 * u[i]**3 + 180 * u[i]**2 - 45 * u[i])*np.cos(np.pi * v[j])
                self.array[i][j][1] = (160 * u[i]**4 - 320 * u[i]**3 + 160 * u[i]**2)
                self.array[i][j][2] = (-90 * u[i]**5 + 225 * u[i]**4 - 270 * u[i]**3 + 180 * u[i]**2 - 45 * u[i])*np.sin(np.pi * v[j])


    def print_array(self):
        print(self.array)
        print(arraySize)
        print(arr)

    def copy_array(self):
        global arr
        arr = self.array

def startup():
    egg = Egg(50)
    egg.fill_array()
    egg.copy_array()
    egg.print_array()
    
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time *180/np.pi)
    axes()
    
    #Zadanie na ocenę 3.0
    # for i in range(arraySize):
    #     for j in range(arraySize):
    #         glColor3f(1.0, 1.0, 1.0)
    #         glBegin(GL_POINTS)
    #         glVertex3f(arr[i][j][0], arr[i][j][1], arr[i][j][2])
    #         glEnd()
    
    
    for i in range(arraySize-1):
        for j in range(arraySize-1):
            glColor3f(1.0, 1.0, 1.0)
            glBegin(GL_POINTS)
            #glVertex3f(arr[i][j][0], arr[i][j][1], arr[i][j][2])
            glVertex3f(arr[i][j][0], arr[i][j][1], arr[i][j][2])
            glEnd()


    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-20, 20, -20 / aspect_ratio, 20 / aspect_ratio, 20, -20)
    else:
        glOrtho(-20 * aspect_ratio, 20 * aspect_ratio, -20, 20, 20, -20)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)
    

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()