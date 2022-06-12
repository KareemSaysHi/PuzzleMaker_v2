'''
Class that deals with piece symmetries
'''

from sympy import Q


class Piece():
    def __init__(self, poly):
        self.piece = poly #1D array with coords
        self.uniqueRots = []

        self.rotationsDict = {
            "wg": lambda x, y, z: (x, y, z), #identity
            "wo": lambda x, y, z: (-y, x, z), #x, y 90 deg rotation from wg
            "wb": lambda x, y, z: (-x, -y, z), #x, y 180 deg rotation from wg
            "wr": lambda x, y, z: (y, -x, z), #x, y 270 deg rotation from wg

            "rg": lambda x, y, z: (-z, y, x), #x, z rotates 90 degrees counterclockwise from identity, y invariant
            "rw": lambda x, y, z: (-y, -z, x), #x, y 90 deg rotation from rg
            "rb": lambda x, y, z: (z, -y, x), #x, y 180 deg rotation from rg
            "ry": lambda x, y, z: (y, z, x), #x, y 270 deg rotation from rg

            "bw": lambda x, y, z: (x, -z, y), #y, z rotates 90 degrees counterclockwise from identity, x invariant
            "bo": lambda x, y, z: (z, x, y), #x, y 90 deg rotation from bw
            "by": lambda x, y, z: (-x, z, y), #x, y 180 deg rotation from bw
            "br": lambda x, y, z: (-z, -x, y), #x, y 270 deg rotation from bw

            "yb": lambda x, y, z: (x, -y, -z), #rotation 180 of wg about x axis
            "yr": lambda x, y, z: (-y, -x, -z), #rotation 180 of wr about x axis
            "yg": lambda x, y, z: (-x, y, -z), #rotation 180 of wb about x axis
            "yo": lambda x, y, z: (y, x, -z), #rotation 180 of wo about x axis

            "ob": lambda x, y, z: (-z, -y, -x), #rotation 180 of rg about x axis
            "oy": lambda x, y, z: (-y, z, -x), #rotation 180 of rw about x axis
            "og": lambda x, y, z: (z, y, -x), #rotation 180 of rb about x axis
            "ow": lambda x, y, z: (y, -z, -x), #rotation 180 of ry about x axis

            "gy": lambda x, y, z: (x, z, -y), #rotation 180 of bw about x axis
            "gr": lambda x, y, z: (z, -x, -y), #rotation 180 of bo about x axis
            "gw": lambda x, y, z: (-x, -z, -y), #rotation 180 of by about x axis
            "go": lambda x, y, z: (-z, x, -y) #rotation 180 of br about x axis
        }

    def getAllCanonicalRots(self):
        rotations = self.getRotations() #get rotations
        
        canonicalPolys = rotations
        for i in range (0, len(canonicalPolys)): #make all rotations canonical
            canonicalPolys[i] = self.canonical(canonicalPolys[i]) #where group[i] is a poly

        return canonicalPolys

    def getSupplementalRot(self, rotNumber): #corresponds to rot key number in dict
        #see long comment in fixRequiredPositionsSymmetryProblem (assembly.py)
        rotation = self.piece.copy()
        
        for i in range(0, 3):
            xCoords = [coord[0] for coord in rotation]
            yCoords = [coord[1] for coord in rotation]
            zCoords = [coord[2] for coord in rotation]

            rotation = list(map(self.rotationsDict[self.rotationsDict.keys()[rotNumber]], xCoords, yCoords, zCoords))

        return rotation

    def determineUniqueRots(self):
        rotations = self.getRotations() #get rotations
        
        canonicalPolys = rotations
        for i in range (0, len(canonicalPolys)): #make all rotations canonical
            canonicalPolys[i] = self.canonical(canonicalPolys[i]) #where group[i] is a poly

        #remove redundancies:
        duplicateLog = []
        for i in range(0, len(canonicalPolys)-1): #basically n choose 2 to compare all possibilities
            for j in range(i+1, len(canonicalPolys)): #note again that polyThisRankCanonical is 3D
                if not self.isUnique(canonicalPolys[i], canonicalPolys[j]):
                    duplicateLog.append((i, j))

        for duplicate in duplicateLog:
            canonicalPolys[duplicate[1]] = None #make the larger number in duplication None
        
        x = 0
        while x < len(canonicalPolys):
            if canonicalPolys[x] == None:
                canonicalPolys.pop(x) #don't add 1 to x here cause length decreased
            else:
                x += 1
        
        self.uniqueRots = canonicalPolys

    def getUniqueRotations(self):
        return self.uniqueRots

    def isUnique(self, poly1, poly2): #tested and works
        if poly1 == poly2:
            return False

        return True

    def getRotations(self): 
        '''
        Returns all different ways to rotate the self.poly (24)
        Inputs: 1D poly array
        Output: 2D array of 24 polys
        '''
        xCoords = [coord[0] for coord in self.piece]
        yCoords = [coord[1] for coord in self.piece]
        zCoords = [coord[2] for coord in self.piece]

        rotationsList = [list(map(self.rotationsDict[key], xCoords, yCoords, zCoords)) for key in list(self.rotationsDict.keys())] # @Nikhil Kalidasu

        return rotationsList

    def canonical(self, poly): #tested and works
        '''
        sorts and brings polyominoes to origin
        Inputs: 1D array with polyomino coords
        Outputs: corrected polyomino
        '''

        poly = sorted(poly, key = lambda x: (x[0], x[1], x[2])) #sort by x first, then y
        
        xCoords = [coord[0] for coord in poly]
        yCoords = [coord[1] for coord in poly]
        zCoords = [coord[2] for coord in poly]

        minX = min(xCoords)
        if minX < 0:
            for i in range (0, len(poly)):
                poly[i] = list(poly[i])
                poly[i][0] -= minX
                poly[i] = tuple(poly[i])
            
        minY = min(yCoords)
        if minY < 0:
            for i in range (0, len(poly)):
                poly[i] = list(poly[i])
                poly[i][1] -= minY
                poly[i] = tuple(poly[i])

        minZ = min(zCoords)
        if minZ < 0:
            for i in range (0, len(poly)):
                poly[i] = list(poly[i])
                poly[i][2] -= minZ
                poly[i] = tuple(poly[i])

        #print(poly)
        return poly

    def getRank(self):
        return len(self.piece)

    def getNumUniqueRotations(self):
        return len(self.uniqueRots)
