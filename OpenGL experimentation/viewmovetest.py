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

    firstFrame = False
    dragLin = False
    dragRot = False

    totalMovementX = 0
    totalMovementY = 0
    totalMovementZ = 0


    glMatrixMode(GL_PROJECTION)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0) #degrees in view, aspect ratio, near clip, far clip


    a = (GLfloat * 16)()
    modelMat = glGetFloatv(GL_MODELVIEW_MATRIX, a)
    
    while True:

        if firstFrame:
            preMx, preMy = pygame.mouse.get_pos()

        glMatrixMode( GL_MODELVIEW );    
        glLoadIdentity()
        
        for event in pygame.event.get(): #event cycle in pygame
            if event.type == pygame.QUIT: 
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragRot = True
                if event.button == 2:
                    dragLin = True
                if event.button == 4:
                    glTranslatef(0, 0, .5)
                    totalMovementZ += .5
                if event.button == 5:
                    glTranslatef(0, 0, -.5)
                    totalMovementZ -= .5

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragRot = False
                if event.button == 2:
                    dragLin = False

        currentMx, currentMy = pygame.mouse.get_pos()
        
        if dragLin:
            deltaMx = currentMx - preMx
            deltaMy = currentMy - preMy
            deltaMx = deltaMx*0.02
            deltaMy = -deltaMy*0.02 #neg cause of how GL has positive going down
            glTranslatef(deltaMx, deltaMy, 0)
            totalMovementX += deltaMx
            totalMovementY += deltaMy

        if dragRot: #ROTATION BEFORE TRANSLATION (before in the sense of matrix transformations)
            deltaMx = currentMx - preMx
            deltaMy = currentMy - preMy

            glTranslatef(totalMovementX, totalMovementY, totalMovementZ) #going back
            glRotatef(deltaMx, 0, 1, 0) #perform rotations about the origin
            glRotatef(deltaMy, 1, 0, 0)
            glTranslatef(-1*totalMovementX, -1*totalMovementY, -1*totalMovementZ) #going there


        glMultMatrixf( modelMat )
        modelMat = glGetFloatv(GL_MODELVIEW_MATRIX, a)

        glLoadIdentity()
        glMultMatrixf( modelMat )

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip() #flip is the equiv of pygame.display.update()
        preMx, preMy = pygame.mouse.get_pos() #must be before wait

        pygame.time.wait(10)

main()