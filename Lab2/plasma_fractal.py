#!/usr/bin/env python3
import sys
import numpy as np
import random
import statistics
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


iteration = 0
'''
Algo to be implemented
    def diamondSquare(height, width):
        Map -> 2D array of 0s
        initialize array with 4 values on the edges
        step_size = width -1
        r -> random value 
            while step_size > 1:
                leap over map
                
                For every square on the map
                    perform diamond_step
                For evety diamond on the map
                    perform square_step
            step_size /= 2
            reduce random range for r

    def diamond_step(x,y,step_size, r):
        avg = average of square corners step_size apart
        map[x+step_size/2][y+step_size/2] = avg + r

    def square_step(x,y,step_size, r):
        avg = avg of four corners of diamond
        map[x][y] = avg + r
        
'''

class Array:
    
    def __init__(self, size, *args, **kwargs):
        self.array = np.zeros((size,size))
        self.size = size

    def print_array(self):
        print(self.array)

    def __decorator(function):
        def initialize_corners(self):
            self.array[0][0] = function()
            self.array[self.size-1][0] = function()
            self.array[self.size-1][self.size-1] = function()
            self.array[0][self.size-1] = function()
            print(self.array)
        return initialize_corners

    @__decorator
    def grayscale_init():
        return random.uniform(0,1)

    @__decorator
    def color_init():
        return (random.uniform(0,1) for i in range(0,3))

    def diamond_step(self, step_size):
        midway_step = step_size // 2

        for i in range(0, self.size, step_size):
            for j in range(0, self.size, step_size):
                if((i + midway_step) < self.size and (j + midway_step) < self.size):
                    upper_left_point = self.array[i][j]
                    upper_right_point = self.array[i + step_size][j]
                    bottom_left_point = self.array[i][j + step_size]
                    bottom_right_point = self.array[i + step_size][j + step_size]
                    #print(f"i:{i} --- j:{j}")
                    #print(i + midway_step)
                    self.array[i + midway_step][j + midway_step] = (upper_left_point +upper_right_point +bottom_left_point +bottom_right_point)/4
                    #self.print_array()
                    #print('-'*30)

    def square_step(self, step_size):
        check_left = lambda i, j, mid_step: 0 if j-mid_step<0 else self.array[i][j-mid_step] #x- współrzędna y-przesunięcie
        check_right = lambda i, j, mid_step: 0 if j+mid_step>self.size-1 else self.array[i][j+mid_step]
        check_up = lambda i, j, mid_step: 0 if i-mid_step<0 else self.array[i-mid_step][j]
        check_down = lambda i, j, mid_step: 0 if i+mid_step>self.size-1 else self.array[i+mid_step][j]
        
        midway_step = step_size//2
        odd_case = False
        for i in range(0, self.size, midway_step):
            x = (lambda condition: midway_step if  not condition else 0)(odd_case)
            #print(odd_case)
            #print(x)
            for j in range (x, self.size, midway_step):
                left_field = check_left(i, j, midway_step)
                right_field = check_right(i, j, midway_step)
                up_field = check_up(i, j, midway_step)
                down_field = check_down(i, j, midway_step)
                if(self.array[j][i]==0 or iteration!=0):
                    self.array[j][i] = (left_field + right_field + up_field + down_field) /4
                    #print(f'[{j}][{i}]: {left_field}, {right_field}, {up_field}, {down_field}')
                #x = sum(self.array[j][i])
                #print(f'{left(j, midway_step)} --- x:{j} ---y:{i}')
            odd_case = not odd_case

    def diamond_square_algorithm(self):
        global iteration
        step_size = self.size-1
        print('='*50)
        print('Size:', step_size, '  Iteration:', iteration)
        self.print_array()
        while step_size > 1:
            self.diamond_step(step_size)
            self.square_step(step_size)
            step_size //=2
        iteration += 1
            

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)
    array = Array(513)
    array.grayscale_init()
    array.diamond_square_algorithm()
    array.print_array()
    print("="*50)
    return array
def shutdown():
    pass
    
def render(time, array):
    array.diamond_square_algorithm()
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(3)
    glBegin(GL_POINTS)
    for i in range(0,array.size):
        for j in range(0,array.size):
            color = array.array[i][j]
            glColor3fv([color, color, color])
            glVertex2f(i * 100.0/array.size, j*100.0/array.size)
    glEnd()
    glFlush()

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

    arr = startup()

    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), arr)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main() 