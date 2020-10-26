#!/usr/bin/env python3
import sys
import numpy as np
import random
import statistics
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


m_size = 1024
array_of_points = np.zeros((m_size,m_size))

def initialize_array(m_size, array):
    array[0][0] = randomize_color_monochromatic()
    array[m_size-1][0] = randomize_color_monochromatic()
    array[m_size-1][m_size-1] = randomize_color_monochromatic()
    array[0][m_size-1] = randomize_color_monochromatic()


def diamond_step(len):
    tmp_length = size/2

def square_step(len, array):
    tmp_length = size/2
    for i in range(0,size//(len-1)):
        for j in range(0,size//(len-1)):
            x_loc = (len-1)*x + tmp_length;
            y_loc = (len-1)*y + tmp_length;

            #color_result = func
            array[x_loc][y_loc] = 1

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)
    initialize_array_monochromatic(m_size, array_of_points)


def shutdown():
    pass

def randomize_color_monochromatic():
    return random.uniform(0,1)
    
def render(time):
    pass
#glFlush()
    
'''
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0, 0.0)
    glVertex2f(0.0, 50.0)
    glVertex2f(50.0, 0.0)
    glEnd()

    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0, 0.0)
    glVertex2f(0.0, 50.0)
    glVertex2f(-50.0, 0.0)
    glEnd()
'''

def update_viewport(window, width, height):
    if height == 0:
        height = 1
    if width == 0:
        width = 1
    aspectRatio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspectRatio, 100.0 / aspectRatio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspectRatio, 100.0 * aspectRatio, -100.0, 100.0,
                1.0, -1.0)

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
