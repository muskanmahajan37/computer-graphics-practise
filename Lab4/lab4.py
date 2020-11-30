#!/usr/bin/env python3
import sys
import numpy as np
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 10.0]

phi = 0.0
theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0
scale = 10
x_eye = 1
z_eye = 1
y_eye = 1
change_mode = True
def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


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


def example_object():
    glColor3f(1.0, 1.0, 1.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)

def set_eyes(R, theta, phi):
    global x_eye, y_eye, z_eye
    x_eye = R * np.cos(abs(theta* np.pi/180)) * np.cos(abs(phi* np.pi/180))
    y_eye = R * np.sin(abs(phi* np.pi/180))
    z_eye = R * np.sin(abs(theta* np.pi/180)) * np.cos(abs(phi* np.pi/180))

def task_3_0_and_3_5():
    global theta, phi, scale
    gluLookAt(viewer[0], viewer[1], viewer[2],
          0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    if left_mouse_button_pressed:
        theta += (delta_x * pix2angle)
        phi += (delta_y * pix2angle)
    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 0.0, 0.0, 1.0)
    if right_mouse_button_pressed:
        scale += delta_y
    glScalef(scale/10, scale/10, scale/10)
    

def task_4_0():
    global scale, theta, phi, x_eye, y_eye, z_eye
    if left_mouse_button_pressed:
        theta += (delta_x * pix2angle)
        phi += (delta_y * pix2angle)
    if right_mouse_button_pressed:
        scale += delta_y
    set_eyes(scale,theta, phi)
    gluLookAt(x_eye, y_eye, z_eye,
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)


def task_4_5():
    global scale, theta, phi, x_eye, y_eye, z_eye
    if change_mode:
        if left_mouse_button_pressed:
            theta += (delta_x * pix2angle)
            phi += (delta_y * pix2angle)
            theta %= 360
            phi %= 360

        if right_mouse_button_pressed:
            if scale <= 20:
                scale += delta_y/5
            else:
                scale = 20
            if scale <0.01:
                scale=0.02
            else:
                scale += delta_y/5

        set_eyes(scale,theta, phi)
        if phi> 90 and phi < 270:
            gluLookAt(x_eye, y_eye, z_eye,
                    0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        else:
            gluLookAt(x_eye, y_eye, z_eye,
                        0.0, 0.0, 0.0, 0.0, -1.0, 0.0)
            #print(f'Theta: {theta}   Phi: {phi}')
    else:
        gluLookAt(viewer[0], viewer[1], viewer[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        if left_mouse_button_pressed:
            theta += (delta_x * pix2angle)
            phi += (delta_y * pix2angle)
        glRotatef(theta, 0.0, 1.0, 0.0)
        glRotatef(phi, 0.0, 0.0, 1.0)
        if right_mouse_button_pressed:
            if scale <= 20:
                scale += delta_y/5
            else:
                scale = 20
            if scale <0.01:
                scale=0.02
            else:
                scale += delta_y/5
        glScalef(scale/10, scale/10, scale/10)


def render(time):
    global theta, phi, scale, x_eye, y_eye, z_eye
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # task_3_0_and_3_5()
    # task_4_0()
    #task_4_5()

    axes()
    example_object()

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global change_mode
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == 67 and action == GLFW_PRESS:
        change_mode = not change_mode


#do modyfikacji
def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global delta_y
    global mouse_x_pos_old
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos
    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed
    global scale

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
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
