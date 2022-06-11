import pygame
from pygame.locals import *
import numpy as np

from OpenGL.GL import * #basic opengl stuff
from OpenGL.GLU import * #more complex opengl stuff 

class GUI():
    def __init__(self, pieceDict = {}, posDict = {}):
        self.pieceDict = pieceDict
        self.posDict = posDict

        self.colorDict = {
            0: (1, 0, 0),
            1: (0, 1, 0),
            2: (0, 0, 1),
            3: (0, 1, 0),
            4: (0, 0, 1),
            5: (0, 1, 1),
            6: (1, 1, 0),
            7: (1, 0, 1)
        }
        
        self.pyDisplay = None

        self.firstFrame = False
        self.dragLin = False
        self.dragRot = False

        self.totalMovementX = 0
        self.totalMovementY = 0
        self.totalMovementZ = 0

        self.initPyGame()

    def initPyGame(self, width=800, height=600):
        pygame.init() #initializes pygame
        self.pyDisplay = (width, height)
        pygame.display.set_mode(self.pyDisplay, DOUBLEBUF|OPENGL) #letting pygame know of openGL usage
        
    def setPiecesAndPos(self, pieceDict, posDict):
        self.pieceDict = pieceDict
        self.posDict = posDict

    def cube(self, pos):
        '''
        Makes a cube given a piece coordinate
        Input: self, pos (3-tuple)
        Output: dict with vertices, edges, surfaces
        '''

        vertices = (
            (pos[0] + 0, pos[1] + 0, pos[2] + 0),
            (pos[0] + 1, pos[1] + 0, pos[2] + 0),
            (pos[0] + 1, pos[1] + 1, pos[2] + 0),
            (pos[0] + 0, pos[1] + 1, pos[2] + 0),
            (pos[0] + 0, pos[1] + 0, pos[2] + 1),
            (pos[0] + 1, pos[1] + 0, pos[2] + 1),
            (pos[0] + 1, pos[1] + 1, pos[2] + 1),
            (pos[0] + 0, pos[1] + 1, pos[2] + 1)
        )

        edges = (
            (0, 1),
            (0, 3),
            (0, 4),
            (2, 1),
            (2, 3),
            (2, 6),
            (1, 5),
            (4, 5),
            (4, 7),
            (6, 7),
            (5, 6),
            (3, 7)
        )

        surfaces = (
            (0, 1, 2, 3),
            (0, 3, 7, 4),
            (3, 2, 6, 7),
            (1, 2, 6, 5),
            (0, 1, 5, 4),
            (4, 5, 6, 7)
        )

        return {
            "vertices": vertices,
            "edges": edges,
            "surfaces": surfaces
        }

    def pieceToOpenGL(self, piece, pos):
        '''
        Takes in coordinates of a piece, and returns a list of dictionaries (each dictionary for every cube needing to be rendered)
        Input: self, piece (tuple of tuples), pos (3-tuple)
        Output: list of dictionaries
        '''
        cubeDicts = [] #a list holding dictionaries, each dictionary defines a cube
        for coord in piece:
            newX = coord[0] + pos[0]
            newY = coord[1] + pos[1]
            newZ = coord[2] + pos[2]
            newCubeDict = self.cube((newX, newY, newZ))
            cubeDicts.append(newCubeDict)
        
        return cubeDicts

    def render(self, fixedColor=False):
        '''
        Given pieceDict and posDict, does all the rendering
        1st: needs to generate cube dictionaries
        2nd: actually draw them
        Inputs: just self
        Output: None
        '''
        
        #drawing surfaces
        glBegin(GL_QUADS)
        
        keys = self.pieceDict.keys()

        for key in keys:
            if fixedColor == False:
                glColor3fv(self.colorDict[key]) #set the color of everything that's being drawn
            else:
                glColor3fv((1, 0, 0)) #set the color of everything that's being drawn
            currentPiece = self.pieceDict[key]
            currentPos = self.posDict[key]
            currentCubeDicts = self.pieceToOpenGL(currentPiece, currentPos) #returns a list of cube dicts

            for cubeDict in currentCubeDicts: #next four lines draw the surfaces of the cube
                for surface in cubeDict["surfaces"]:
                    for vertex in surface:
                        glVertex3fv(cubeDict["vertices"][vertex])

        glEnd()

        #drawing wire frames
        glBegin(GL_LINES)

        glColor3fv((0, 0, 0)) #set wire frame color

        for key in keys:
            currentPiece = self.pieceDict[key]
            currentPos = self.posDict[key]
            currentCubeDicts = self.pieceToOpenGL(currentPiece, currentPos) #returns a list of cube dicts

            for cubeDict in currentCubeDicts: #next four lines draw the edges of the cube
                for edge in cubeDict["edges"]:
                    for vertex in edge:
                        glVertex3fv(cubeDict["vertices"][vertex])
                                 
        glEnd()

    def showScreen(self, fixedColor=False):
        '''
        performs all the necessary things for camera movement, rotation around origin, pan, zoom
        input: self
        output: None
        '''
        
        glMatrixMode(GL_PROJECTION)

        gluPerspective(45, (self.pyDisplay[0]/self.pyDisplay[1]), 0.1, 50.0) #degrees in view, aspect ratio, near clip, far clip

        a = (GLfloat * 16)()
        modelMat = glGetFloatv(GL_MODELVIEW_MATRIX, a)

        while True:

            if self.firstFrame:
                preMx, preMy = pygame.mouse.get_pos()

            glMatrixMode( GL_MODELVIEW );    
            glLoadIdentity()
            
            for event in pygame.event.get(): #event cycle in pygame
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.dragRot = True
                    if event.button == 2:
                        self.dragLin = True
                    if event.button == 4:
                        glTranslatef(0, 0, .5) #make sure to change both of these rather than just one
                        self.totalMovementZ += .5
                    if event.button == 5:
                        glTranslatef(0, 0, -.5)
                        self.totalMovementZ -= .5

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.dragRot = False
                    if event.button == 2:
                        self.dragLin = False
            
            currentMx, currentMy = pygame.mouse.get_pos()
            
            if self.dragLin:
                deltaMx = currentMx - preMx
                deltaMy = currentMy - preMy
                deltaMx = deltaMx*0.02
                deltaMy = -deltaMy*0.02 #neg cause of how GL has positive going down
                glTranslatef(deltaMx, deltaMy, 0)
                self.totalMovementX += deltaMx
                self.totalMovementY += deltaMy

            if self.dragRot: #ROTATION BEFORE TRANSLATION (before in the sense of matrix transformations)
                deltaMx = currentMx - preMx
                deltaMy = currentMy - preMy

                glTranslatef(self.totalMovementX, self.totalMovementY, self.totalMovementZ) #going back
                glRotatef(deltaMx, 0, 1, 0) #perform rotations about the origin
                glRotatef(deltaMy, 1, 0, 0)
                glTranslatef(-1*self.totalMovementX, -1*self.totalMovementY, -1*self.totalMovementZ) #going there

            glMultMatrixf( modelMat )
            modelMat = glGetFloatv(GL_MODELVIEW_MATRIX, a)

            glLoadIdentity()
            glMultMatrixf( modelMat )

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            self.render(fixedColor)
            pygame.display.flip() #flip is the equiv of pygame.display.update()

            preMx, preMy = pygame.mouse.get_pos() #must be before wait
            
            pygame.time.wait(10)

'''
def main():

    pieces = {
        0: [
            (0, 0, 0),
            (0, 0, 1),
            (0, 1, 1),
            (1, 1, 1),
        ],

        1: [
            (0, 0, 0),
            (0, 1, 0),
            (1, 1, 0),
            (1, 1, 1),
        ]
    }

    pos = {
        0: (0, 0, 0),
        1: (0, 3, 0)
    }

    gui = GUI(pieces, pos)
    gui.showScreen()

main()
'''

