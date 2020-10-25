#!/usr/bin/env python3
import sys
import numpy as np
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

m_size = 5
array_of_points = np.zeros((m_size,m_size))

def initialize_array_monochromatic(m_size, array):
    array[0][0] = randomize_color_monochromatic()
    array[m_size-1][0] = randomize_color_monochromatic()
    array[m_size-1][m_size-1] = randomize_color_monochromatic()
    array[0][m_size-1] = randomize_color_monochromatic()

def generate_other_vertecies(array, ax, ay, bx, by, cx, cy, dx, dy):
    new_wx = ax
    new_wy = (by-1-ay)//2
    new_xx = cx-1
    new_xy = (dy-1-cy)//2
    new_yx = (cx-1-ax)//2
    new_yy = ay
    new_zx = (dx-1-bx)//2
    new_zy = dy-1
    new_qx = (cx-1-ax)//2
    new_qy = (by-1-ay)//2
    if(array[new_wx][new_wy] == 0): array[new_wx][new_wy] = randomize_color_monochromatic()
    if(array[new_xx][new_xy] == 0): array[new_xx][new_xy] = randomize_color_monochromatic()
    if(array[new_yx][new_yy] == 0): array[new_yx][new_yy] = randomize_color_monochromatic()
    if(array[new_zx][new_zy] == 0): array[new_zx][new_zy] = randomize_color_monochromatic()
    if(array[new_qx][new_qy] == 0): array[new_qx][new_qy] = randomize_color_monochromatic()

    generate_other_vertecies
    print(array)

''' 
    '''
def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)
    initialize_array_monochromatic(m_size, array_of_points)

    generate_other_vertecies(array_of_points,0,0,0,m_size,m_size,0,m_size,m_size)


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
