import pygame
from pygame.locals import *

from OpenGL.GL import * #basic opengl stuff
from OpenGL.GLU import * #more complex opengl stuff 

verticies = (
    (1, -1, -1), #this is node 0
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

colors = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 0, 0),
    (1, 1, 1),
    (0, 1, 1),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 0, 0),
    (1, 1, 1),
    (0, 1, 1)
)

def Cube():
    glBegin(GL_QUADS)
    
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x += 1          
            glColor3fv(colors[x])  
            glVertex3fv(verticies[vertex])
    glEnd()
    
    glBegin(GL_LINES) #you need this every time you do gl code

    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])

    glEnd()

def main():
    pygame.init() #initializes pygame
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL) #you need to let pygame know that opengl is coming

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0) #degrees in view, aspect ratio, near clip, far clip

    glTranslatef(0.0, 0.0, -10) #moving ourselves back -5 in z

    glRotatef(25, 2, 1, 0)

    while True:
        for event in pygame.event.get(): #event cycle in pygame
            if event.type == pygame.QUIT: 
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glTranslatef(-.5, 0, 0)
                if event.key == pygame.K_RIGHT:
                    glTranslatef(.5, 0, 0)

                if event.key == pygame.K_UP:
                    glTranslatef(0, .5, 0)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0, -.5, 0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0, 0, .5)
                if event.button == 5:
                    glTranslatef(0, 0, -.5)


        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #glRotatef(1, 3, 1, 1)
        Cube()
        pygame.display.flip() #flip is the equiv of pygame.display.update()
        pygame.time.wait(10)

main()