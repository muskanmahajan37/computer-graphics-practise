#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
import random

lista = [0.0,1.0,1.0]

class rectangle:

    def __init__(x_of_center,y_of_center, width, height):
        self.x1 = x_of_center + width/2
        self.y1 = y_of_center + height/2
        
        self.x2 = x_of_center - width/2
        self.y2 = y_of_center - height/2
        
        self.x3 = x_of_center + width/2
        self.y3 = y_of_center - height/2
        
        self.x4 = x_of_center - width/2
        self.y4 = y_of_center + height/2

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)

def shutdown():
    pass

def draw_rectangle(x_of_center,y_of_center, width, height):
    nodes = {
        'node0': (x_of_center + width/2, y_of_center + height/2, [1.0, 0.0, 0.0]),
        'node1': (x_of_center - width/2, y_of_center + height/2, [0.0 , 0.0, 1.0]),
        'node2': (x_of_center + width/2, y_of_center - height/2, [0.0, 0.0, 1.0]),
        'node3': (x_of_center - width/2, y_of_center - height/2, [1.0, 0.0, 0.0]),
    }

    glBegin(GL_TRIANGLES)
    glColor3fv(nodes['node0'][2])
    glVertex2f(nodes['node0'][0], nodes['node0'][1])
    glColor3fv(nodes['node1'][2])
    glVertex2f(nodes['node1'][0], nodes['node1'][1])
    glColor3fv(nodes['node2'][2])
    glVertex2f(nodes['node2'][0], nodes['node2'][1])
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3fv(nodes['node1'][2])
    glVertex2f(nodes['node1'][0], nodes['node1'][1])
    glColor3fv(nodes['node2'][2])
    glVertex2f(nodes['node2'][0], nodes['node2'][1])
    glColor3fv(nodes['node3'][2])
    glVertex2f(nodes['node3'][0], nodes['node3'][1])
    glEnd()

    glFlush()

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    draw_rectangle(0,0,50.0,80.0)
    
'''
    glColor3fv(lista)
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(-120.0, -70.0)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(120.0, -70.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(0, 100)
    glEnd()
    
    glFlush()
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
