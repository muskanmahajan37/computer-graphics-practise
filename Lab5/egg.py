import sys

from glfw.GLFW import *
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from random import random

global arraySize
global arr

'''
Opis do zadań:
-Poruszanie źródłem światała odbywa się za pomocą myszki,
-Zmiana parametrów koloru       (klawisze 1-9)
-Przełącznik zmienianego źródła (klawisz C)
-Zwiększenie/mniejszenie wartości   (klawisze +/- na klawiaturze numerycznej)

Zadanie 4.5, 5.0 'exclusive'
-Przełącznik włączania wektorów normalnych (klawisz D)

Obracanie obiektu, światło statyczne - odkomentować sekcję 1, zakomentować sekcję 2
Wstrzymanie obiektu, światło dynamiczne - odkomentować sekcję 2, zakomentować sekcję 1
'''


viewer = [0.0, 0.0, 10.0]
active_selection = [0, 0]
light_switch_mode = True
light_info = 'light 0'

phi = 0.0
theta = 0.0
pix2angle = 1.0
R_1 = 10.0
R_2 = 10.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_y = 0
delta_x = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 10.0, 0.0, 1.0]

light1_ambient = [0.1, 0.1, 0.0, 1.0]
light1_diffuse = [0.8, 0.1, 0.8, 1.0]
light1_specular = [1.0, 1.0, 1.0, 1.0]
light1_position = [15.0, 10.0, 0.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

light_params_list = [
    light_ambient,
    light_diffuse,
    light_specular,
    light1_ambient,
    light1_diffuse,
    light1_specular
]

light_sources_coordinates = {
    'source_1': [R_1 * np.cos(theta * np.pi / 360) * np.cos(phi * np.pi / 360),  # x_s0
                 R_1 * np.sin(phi * np.pi / 360),  # y_s0
                 R_1 * np.sin(theta * np.pi / 360) * np.cos(phi * np.pi / 360),
                 1.0],  # z_s0
    'source_2': [-R_2 * np.cos(theta * np.pi / 360) * np.cos(phi * np.pi / 360),  # x_s1
                 -R_2 * np.sin(phi * np.pi / 360),  # y_s1
                 -R_2 * np.sin(theta * np.pi / 360) * np.cos(phi * np.pi / 360),
                 1.0],  # z_s1
}


def first_light_source():
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_sources_coordinates['source_1'])

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)


def second_light_source():
    glLightfv(GL_LIGHT1, GL_AMBIENT, light1_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light1_diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light1_specular)
    glLightfv(GL_LIGHT1, GL_POSITION, light_sources_coordinates['source_2'])

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)


class Egg:
    def __init__(self, size):
        self.array = np.zeros((size, size, 6))
        global arraySize
        arraySize = size
        self.denormalized_vector = [0.0, 0.0, 0.0]
        self.normalized_vectors = np.zeros((size, size), dtype=object)
        self.display_norm_vectors = False

    def fill_array(self):
        u = [i / (arraySize - 1) for i in range(arraySize)]
        v = [i / (arraySize - 1) for i in range(arraySize)]

        for i in range(0, arraySize):
            for j in range(0, arraySize):
                self.array[i][j][0] = (-90 * u[i] ** 5 + 225 * u[i] ** 4 - 270 * u[i] ** 3 + 180 * u[i] ** 2 - 45 * u[
                    i]) * np.cos(np.pi * v[j])
                self.array[i][j][1] = (160 * u[i] ** 4 - 320 * u[i] ** 3 + 160 * u[i] ** 2) - 4
                self.array[i][j][2] = (-90 * u[i] ** 5 + 225 * u[i] ** 4 - 270 * u[i] ** 3 + 180 * u[i] ** 2 - 45 * u[
                    i]) * np.sin(np.pi * v[j])
                self.array[i][j][3] = 1
                self.array[i][j][4] = 1
                self.array[i][j][5] = 1
                x_u = (-450 * (u[i] ** 4) + 900 * (u[i] ** 3) - 810 * (u[i] ** 2) + 360 * u[i] - 45) \
                      * np.cos(np.pi * v[j])
                y_u = 640 * (u[i] ** 3) - 960 * (u[i] ** 2) + 320 * u[i]
                z_u = (-450 * (u[i] ** 4) + 900 * (u[i] ** 3) - 810 * (u[i] ** 2) + 360 * u[i] - 45) \
                      * np.sin(np.pi * v[j])

                x_v = np.pi * (90 * (u[i] ** 5) - 225 * (u[i] ** 4) + 270 * (u[i] ** 3) - 180 * (u[i] ** 2) + 45 * u[i]) \
                      * np.sin(np.pi * v[j])
                y_v = 0
                z_v = - np.pi * (
                        90 * (u[i] ** 5) - 225 * (u[i] ** 4) + 270 * (u[i] ** 3) - 180 * (u[i] ** 2) + 45 * u[i]) \
                      * np.cos(np.pi * v[j])

                self.denormalized_vector[0] = y_u * z_v - z_u * y_v
                self.denormalized_vector[1] = z_u * x_v - x_u * z_v
                self.denormalized_vector[2] = x_u * y_v - y_u * x_v
                vector_length = np.sqrt(self.denormalized_vector[0] ** 2
                                        + self.denormalized_vector[1] ** 2
                                        + self.denormalized_vector[2] ** 2)

                if i < arraySize / 2:
                    self.normalized_vectors[i][j] = [
                        self.denormalized_vector[0] / vector_length,
                        self.denormalized_vector[1] / vector_length,
                        self.denormalized_vector[2] / vector_length
                    ]

                elif i == arraySize/2:
                    self.normalized_vectors[i][j] = [0, 1, 0]

                elif i > arraySize/2:
                    self.normalized_vectors[i][j] = [
                        -self.denormalized_vector[0] / vector_length,
                        -self.denormalized_vector[1] / vector_length,
                        -self.denormalized_vector[2] / vector_length
                    ]
                elif i == arraySize or i == 0:
                    self.normalized_vectors[i][j] = [0, -1, 0]

        for i in range(0, arraySize):
            for j in range(0, 2):
                self.array[i][arraySize - 1 - j][3] = self.array[arraySize - 1 - i][j][3]
                self.array[i][arraySize - 1 - j][4] = self.array[arraySize - 1 - i][j][4]
                self.array[i][arraySize - 1 - j][5] = self.array[arraySize - 1 - i][j][5]

    def print_array(self):
        print(self.array)
        print(arraySize)
        print(arr)

    def copy_array(self):
        global arr
        arr = self.array


egg = Egg(30)


def startup():
    global egg
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
    global theta, phi, egg
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += 2 * delta_x * pix2angle
        phi += 2 * delta_y * pix2angle

    axes()

    # #Sekcja 1
    # first_light_source()
    # second_light_source()
    # glRotatef(theta, 0.0, 1.0, 0.0)
    # glRotatef(phi, 0.0, 0.0, 1.0)
    # #end sekcja 1

    for i in range(arraySize - 1):
        for j in range(arraySize - 1):
            glBegin(GL_TRIANGLES)
            glColor3f(arr[i][j][3], arr[i][j][4], arr[i][j][5])
            glNormal3f(egg.normalized_vectors[i][j][0], egg.normalized_vectors[i][j][1],
                       egg.normalized_vectors[i][j][2])
            glVertex3f(arr[i][j][0], arr[i][j][1], arr[i][j][2])
            glColor3f(arr[i][j + 1][3], arr[i][j + 1][4], arr[i][j + 1][5])
            glNormal3f(egg.normalized_vectors[i][j + 1][0], egg.normalized_vectors[i][j + 1][1],
                       egg.normalized_vectors[i][j + 1][2])
            glVertex3f(arr[i][j + 1][0], arr[i][j + 1][1], arr[i][j + 1][2])
            glColor3f(arr[i + 1][j][3], arr[i + 1][j][4], arr[i + 1][j][5])
            glNormal3f(egg.normalized_vectors[i + 1][j][0], egg.normalized_vectors[i + 1][j][1],
                       egg.normalized_vectors[i + 1][j][2])
            glVertex3f(arr[i + 1][j][0], arr[i + 1][j][1], arr[i + 1][j][2])
            glEnd()

            glBegin(GL_TRIANGLES)
            glColor3f(arr[i][j + 1][3], arr[i][j + 1][4], arr[i][j + 1][5])
            glNormal3f(egg.normalized_vectors[i][j + 1][0], egg.normalized_vectors[i][j + 1][1],
                       egg.normalized_vectors[i][j + 1][2])
            glVertex3f(arr[i][j + 1][0], arr[i][j + 1][1], arr[i][j + 1][2])
            glColor3f(arr[i + 1][j][3], arr[i + 1][j][4], arr[i + 1][j][3])
            glNormal3f(egg.normalized_vectors[i + 1][j][0], egg.normalized_vectors[i + 1][j][1],
                       egg.normalized_vectors[i + 1][j][2])
            glVertex3f(arr[i + 1][j][0], arr[i + 1][j][1], arr[i + 1][j][2])
            glColor3f(arr[i + 1][j + 1][3], arr[i + 1][j + 1][4], arr[i + 1][j + 1][3])
            glNormal3f(egg.normalized_vectors[i + 1][j + 1][0], egg.normalized_vectors[i + 1][j + 1][1],
                       egg.normalized_vectors[i + 1][j + 1][2])
            glVertex3f(arr[i + 1][j + 1][0], arr[i + 1][j + 1][1], arr[i + 1][j + 1][2])
            glEnd()

            if egg.display_norm_vectors:
                glBegin(GL_LINES)
                glColor(0.0, 0.0, 0.0)
                glVertex3f(arr[i][j][0], arr[i][j][1], arr[i][j][2])
                glColor(0.0, 0.0, 0.0)
                glVertex3f(arr[i][j][0] + egg.normalized_vectors[i][j][0],
                           arr[i][j][1] + egg.normalized_vectors[i][j][1],
                           arr[i][j][2] + egg.normalized_vectors[i][j][2])
                glEnd()

    glRotatef(theta, 0.0, 1.0, 0.0)  # Zakomentować w celu zablokowania obiektu, a włączenia poruszania źródłem światła
    glRotatef(phi, 0.0, 0.0, 1.0)
    #sekcja 2
    first_light_source()
    second_light_source()
    glTranslate(-light_sources_coordinates['source_1'][0],
                -light_sources_coordinates['source_1'][1],
                light_sources_coordinates['source_1'][2])
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)

    glTranslate(-light_sources_coordinates['source_2'][0],
                -light_sources_coordinates['source_2'][1],
                light_sources_coordinates['source_2'][2])
    glTranslate(-light_sources_coordinates['source_2'][0],
                -light_sources_coordinates['source_2'][1],
                -light_sources_coordinates['source_2'][2])
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)
    #end sekcja 2
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


def keyboard_key_callback(window, key, scancode, action, mods):
    global light_params_list, light_switch_mode, light_info, active_selection
    info = 'Currently changed parameter: '
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_C and action == GLFW_PRESS:
        light_switch_mode = not light_switch_mode
        if light_switch_mode:
            light_info = 'Light 0'
            active_selection[0] -= 3
        else:
            light_info = 'Light 1'
            active_selection[0] += 3
        print(f'Switching to: {light_info}')
        print(light_params_list)
    if key == GLFW_KEY_1 and action == GLFW_PRESS:
        if light_switch_mode:
            active_selection = [0, 0]
        else:
            active_selection = [3, 0]
        print(info, 'light_ambient[0]')
    if key == GLFW_KEY_2 and action == GLFW_PRESS:
        if light_switch_mode:
            active_selection = [0, 1]
        else:
            active_selection = [3, 1]
        print(info, 'light_ambient[1]')
    if key == GLFW_KEY_3 and action == GLFW_PRESS:
        if light_switch_mode:
            active_selection = [0, 2]
        else:
            active_selection = [3, 2]
        print(info, 'light_ambient[2]')
    if key == GLFW_KEY_4 and action == GLFW_PRESS:
        if light_switch_mode:
            active_selection = [1, 0]
        else:
            active_selection = [4, 0]
        print(info, 'light_diffuse[0]:')
    if key == GLFW_KEY_5 and action == GLFW_PRESS:
        if light_switch_mode:
            active_selection = [1, 1]
        else:
            active_selection = [4, 1]
        print(info, 'light_diffuse[1]:')
    if key == GLFW_KEY_6 and action == GLFW_PRESS:
        if light_switch_mode:
            active_selection = [1, 2]
        else:
            active_selection = [4, 2]
        print(info, 'light_diffuse[2]:')
    if key == GLFW_KEY_7 and action == GLFW_PRESS:
        if light_switch_mode:
            active_selection = [2, 0]
        else:
            active_selection = [5, 0]
        print(info, 'light_specular[0]')
    if key == GLFW_KEY_8 and action == GLFW_PRESS:
        if light_switch_mode:
            active_selection = [2, 1]
        else:
            active_selection = [5, 1]
        print(info, 'light_specular[1]')
    if key == GLFW_KEY_9 and action == GLFW_PRESS:
        if light_switch_mode:
            active_selection = [2, 2]
        else:
            active_selection = [5, 2]
        print(info, 'light_specular[2]')

    if key == GLFW_KEY_KP_ADD and action == GLFW_PRESS:
        if np.round(light_params_list[active_selection[0]][active_selection[1]], decimals=1) != 1.0:
            light_params_list[active_selection[0]][active_selection[1]] += 0.1
            print(f'Current value: {np.round(light_params_list[active_selection[0]][active_selection[1]], decimals=1)}')
        else:
            print('reached max value!')
    if key == GLFW_KEY_KP_SUBTRACT and action == GLFW_PRESS:
        if np.round(light_params_list[active_selection[0]][active_selection[1]], decimals=1) != 0.0:
            light_params_list[active_selection[0]][active_selection[1]] -= 0.1
            print(f'Current value: {np.round(light_params_list[active_selection[0]][active_selection[1]], decimals=1)}')
        else:
            print('reached min value!')

    if key == GLFW_KEY_D and action == GLFW_PRESS:
        egg.display_norm_vectors = not egg.display_norm_vectors


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

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


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
