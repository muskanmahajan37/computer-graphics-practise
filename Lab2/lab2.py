#!/usr/bin/env python3
import sys
import time as tajm

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


def draw_carpet(x_center, y_center, width, height, color, self_similarity = 0):
    if self_similarity != 0:
        draw_carpet(x_center - width/3, y_center+height/3, width/3, height/3, color,self_similarity-1)
        draw_carpet(x_center, y_center+height/3, width/3, height/3, color, self_similarity-1)
        draw_carpet(x_center + width/3, y_center+height/3, width/3, height/3, color, self_similarity-1)
        draw_carpet(x_center - width/3, y_center, width/3, height/3, color, self_similarity-1)
        draw_carpet(x_center + width/3, y_center, width/3, height/3, color, self_similarity-1)
        draw_carpet(x_center - width/3, y_center-height/3, width/3, height/3, color, self_similarity-1)
        draw_carpet(x_center, y_center-height/3, width/3, height/3, color, self_similarity-1)
        draw_carpet(x_center + width/3, y_center-height/3, width/3, height/3, color, self_similarity-1)
    else:
        if not color:
            color = draw_rectangle(x_center, y_center, width, height, color)
        draw_rectangle(x_center, y_center, width, height, color)


def draw_rectangle(x_of_center,y_of_center, width, height, color, d = 1):
    colors = []
    if(not color):
        for i in range(0,4):
            colors.append([
                        random.random(),
                        random.random(),
                        random.random()
                        ])
        return colors
    
    nodes = {
        'node0': (x_of_center + width/2*d, y_of_center + height*d/2, color[0]),
        'node1': (x_of_center - width/2*d, y_of_center + height/2*d, color[1]),
        'node2': (x_of_center + width/2*d, y_of_center - height/2*d, color[2]),
        'node3': (x_of_center - width/2*d, y_of_center - height/2*d, color[3])
    }

    glBegin(GL_TRIANGLES)
    glColor3fv(nodes['node0'][2])
    glVertex2f(nodes['node0'][0], nodes['node0'][1])
    glColor3fv(nodes['node1'][2])
    glVertex2f(nodes['node1'][0], nodes['node1'][1])
    glColor3fv(nodes['node2'][2])
    glVertex2f(nodes['node2'][0], nodes['node2'][1])
    glEnd()
#comment
    glBegin(GL_TRIANGLES)   
    glColor3fv(nodes['node1'][2])
    glVertex2f(nodes['node1'][0], nodes['node1'][1])
    glColor3fv(nodes['node2'][2])
    glVertex2f(nodes['node2'][0], nodes['node2'][1])
    glColor3fv(nodes['node3'][2])
    glVertex2f(nodes['node3'][0], nodes['node3'][1])
    glEnd()

    glFlush()
    return colors


def render(time, colors):
    glClear(GL_COLOR_BUFFER_BIT)
    #colors = draw_rectangle(0,0,50.0,50.0, colors)
    draw_carpet(0,0,150.0,150.0,[],int(sys.argv[1]))
    tajm.sleep(1)
'''
    #Zadanie 1
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
    colors = []
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
        render(glfwGetTime(), colors=colors)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main() 
