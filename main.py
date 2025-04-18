from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math

# initial joint angles
shoulder_angle = 90
elbow_angle = 0
wrist_angle = 0

# arm segment lengths
upper_arm_len = 0.4
forearm_len = 0.3
hand_len = 0.2

mouse_button = None
last_x = 0

def draw_circle(radius=0.01, segments=20):
    glBegin(GL_POLYGON)
    for i in range(segments):
        theta = 2.0 * math.pi * i / segments
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        glVertex2f(x, y)
    glEnd()

def draw_segment(length):
    glBegin(GL_POLYGON)
    glVertex2f(-0.008, 0) 
    glVertex2f(0.008, 0) 
    glVertex2f(0.008, -length)
    glVertex2f(-0.008, -length)
    glEnd()

def draw_arm():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    # start positon of the arm
    glTranslatef(-0.2, 0.1, 0.0)

    # SHOULDER
    glPushMatrix()
    glRotatef(shoulder_angle, 0, 0, 1)
    glColor3f(0, 0, 0)
    draw_segment(upper_arm_len)
    glColor3f(1, 0, 0)
    draw_circle()  

    # Move to elbow position
    glTranslatef(0, -upper_arm_len, 0)

    # ELBOW
    glRotatef(elbow_angle, 0, 0, 1)
    glColor3f(0, 0, 0)
    draw_segment(forearm_len)
    glColor3f(0, 1, 0)
    draw_circle() 

    # Move to wrist position
    glTranslatef(0, -forearm_len, 0)

    # WRIST
    glRotatef(wrist_angle, 0, 0, 1)
    glColor3f(0, 0, 0)
    draw_segment(hand_len)
    glColor3f(0, 0, 1)
    draw_circle()  

    glPopMatrix()
    glutSwapBuffers()

def mouse(button, state, x, y):
    global mouse_button, last_x
    if state == GLUT_DOWN:
        mouse_button = button
        last_x = x
    else:
        mouse_button = None

def keyboard(key, x, y):
    global shoulder_angle, elbow_angle, wrist_angle

    if key == b'r':
        shoulder_angle = 90
        elbow_angle = 0
        wrist_angle = 0
        glutPostRedisplay() 

def motion(x, y):
    global shoulder_angle, elbow_angle, wrist_angle, last_x

    dx = x - last_x
    last_x = x

    speed = 0.2  # control sensitivity

    if mouse_button == GLUT_LEFT_BUTTON:
        shoulder_angle += dx * speed
    elif mouse_button == GLUT_RIGHT_BUTTON:
        elbow_angle += dx * speed
    elif mouse_button == GLUT_MIDDLE_BUTTON:
        wrist_angle += dx * speed
    elif keyboard == b'r':
        shoulder_angle = 90
        elbow_angle = 0
        wrist_angle = 0

    glutPostRedisplay()

def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(1000, 750)
    glutCreateWindow(b"2D Robotic Arm")
    init()
    glutDisplayFunc(draw_arm)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutKeyboardFunc(keyboard)  
    glutMainLoop()

if __name__ == "__main__":
    main()
