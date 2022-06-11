import time
import os
import os.path

class Enumerator():

    def __init__(self):
        self.startTime = time.time()

        self.monocubes = [[(0, 0, 0)]]
        self.bicubes = [[(0, 0, 0), (1, 0, 0)]]
        self.tricubes = [[(0, 0, 0), (1, 0, 0), (1, 1, 0)], [(0, 0, 0), (1, 0, 0), (2, 0, 0)]]

        self.rotationsAndReflectionsDict = {
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


    def generateRankWithBounds(self, n, boundingBox=[3, 3, 3], overrideTextFile=False):
        '''
        generates all polyominos of rank n that fit within a bounding box
        inputs: rank, 3D bounding box array
        output: 2D list of polyominoes
        '''

        if n < 0: #catch some basic input errors
            raise ValueError("rank must be greater than 0")
        if boundingBox[0]*boundingBox[1]*boundingBox[2] < n:
            raise ValueError("boundingBox too small to contain such a large rank")

        if n == 0:
            return []
        if n == 1:
            return self.monocubes
        if n == 2:
            return self.bicubes
        if n == 3:
            return self.tricubes
        
        boundingBox.sort(reverse=True)
        for i in range (0, len(boundingBox)):
            if boundingBox[i] > n:
                boundingBox[i] = n #equivalent bounding box, better for matching files
        fileName = "polyList_rank_" + str(n) + "_bounds_" + str(boundingBox[0]) + "_" + str(boundingBox[1]) + "_" + str(boundingBox[2]) + ".txt"

        if os.path.exists("polyLists/" + str(fileName)): #if the data already exists
            polyThisRankFinal = self.readDataFromFile(fileName)
            print("found existing data for rank " + str(n))
            return polyThisRankFinal
        
        polyLastRank = self.generateRankWithBounds(n-1, boundingBox)

        #get all next polyominoes
        polyThisRankUnfiltered = []
        for poly in polyLastRank:
            incomingPolys = self.nextPolycubes(poly, boundingBox)
            for incomingPoly in incomingPolys:
                polyThisRankUnfiltered.append(incomingPoly)

        #get all rotations and reflections
        polyThisRankRotationsAndReflections = []
        for poly in polyThisRankUnfiltered:
            polyThisRankRotationsAndReflections.append(self.rotationsAndReflections(poly)) #this is a 3d array
        
        
        polyThisRankCanonical = polyThisRankRotationsAndReflections
        #make everything canonical
        for group in polyThisRankCanonical:
            for i in range (0, len(group)): #need len cause we can't edit poly otherwise
                group[i] = self.canonical(group[i]) #where group[i] is a poly
                
        #remove redundancies:
        duplicateLog = []
        for i in range(0, len(polyThisRankCanonical)-1): #basically n choose 2 to compare all possibilities
            for j in range(i+1, len(polyThisRankCanonical)): #note again that polyThisRankCanonical is 3D
                if not self.isUnique(polyThisRankCanonical[i], polyThisRankCanonical[j]):
                    duplicateLog.append((i, j))

        for duplicate in duplicateLog:
            polyThisRankCanonical[duplicate[1]] = None #make the larger number in duplication None
        
        x = 0
        while x < len(polyThisRankCanonical):
            if polyThisRankCanonical[x] == None:
                polyThisRankCanonical.pop(x) #don't add 1 to x here cause length decreased
            else:
                x += 1
        
        #get rid of rotation and reflection clutter, return final polyominoes
        polyThisRankFinal = [polyGroup[0] for polyGroup in polyThisRankCanonical]
        print("finished rank " + str(n))

        #write data to file
        self.writeDataToFile(fileName, polyThisRankFinal)

        return polyThisRankFinal

    def writeDataToFile(self, fileName, polyList):
        '''
        Writes final polyList to file in folder polyList
        Input: fileName, polyList
        Output: None
        '''

        with open("polyLists/" + str(fileName), 'w') as f:
            for i in range (0, len(polyList)):
                for j in range (0, len(polyList[i])):
                    f.write(str(polyList[i][j][0]) + "," + str(polyList[i][j][1]) + "," + str(polyList[i][j][2]))
                    if j != len(polyList[i]) - 1:
                        f.write(str(";")) #write semicolon for all but last coord
                if i != len(polyList) - 1:
                    f.write("\n") #write \n for all but last line
            f.close()
    
    def readDataFromFile(self, fileName):
        '''
        Reads from already created file
        Input: fileName
        Output: polyList
        '''

        with open("polyLists/" + str(fileName), 'r') as f:
            lines = f.readlines()
            polyList = []
            for line in lines:
                splitted = line.split(';') #splitted 1D array with "x,y,z" in each index
                for i in range (0, len(splitted)):
                    splitted[i] = tuple(map(int, splitted[i].split(',')))
                polyList.append(splitted)
            f.close()
        
        return polyList

    def isUnique(self, polyGroup1, polyGroup2): #tested and works
        '''
        Takes in two polyGroups (rots and reflections), and sees if they are the same
        Inputs: Two 2D array poly groups
        Outputs: bool True or Falses
        '''

        for poly in polyGroup1:
            if poly in polyGroup2:
                return False

        return True

    #color notation corresponds to the U and F face of a rubiks cube:
    #w = white, y = yellow, g = green, b = blue, r = red, o = orange
    #imagine polyomino sitting fixed on yellow face



    def rotationsAndReflections(self, poly): #tested, I think it works?
        '''
        Takes in a polyomino, returns all different ways to rotate/reflect it (24)
        Inputs: 1D poly array
        Output: a lot
        '''

        xCoords = [coord[0] for coord in poly]
        yCoords = [coord[1] for coord in poly]
        zCoords = [coord[2] for coord in poly]

        rotationsAndReflectionsList = [list(map(self.rotationsAndReflectionsDict[key], xCoords, yCoords, zCoords)) for key in list(self.rotationsAndReflectionsDict.keys())] # @Nikhil Kalidasu

        return rotationsAndReflectionsList

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

    def nextPolycubes(self, poly, boundingBox): #tested and works
        '''
        Given a polycube of rank n, returns all possible extensions of the polycube with rank n+1
        Addition to bound case: requires polycube to be in a bounding box
        Inputs: 1D array with polyomino coords
        Output: list of polyominoes 
        '''
        newCube = lambda x, y, z: [(x-1, y, z), (x+1, y, z), (x, y-1, z), (x, y+1, z), (x, y, z-1), (x, y, z+1)]

        xCoords = [coord[0] for coord in poly]
        yCoords = [coord[1] for coord in poly]
        zCoords = [coord[2] for coord in poly]

        xMin = min(xCoords)
        yMin = min(yCoords)
        xMax = max(xCoords)
        yMax = max(yCoords)
        zMin = min(zCoords)
        zMax = max(zCoords)


        newCubes = list(map(newCube, xCoords, yCoords, zCoords)) #2d array
        
        polyRankUp = []
        for neighborhood in newCubes:
            for nextCoord in neighborhood:
                if abs(xMin - nextCoord[0]) < boundingBox[0] and \
                    abs(xMax - nextCoord[0]) < boundingBox[0] and \
                    abs(yMin - nextCoord[1]) < boundingBox[1] and \
                    abs(yMax - nextCoord[1]) < boundingBox[1] and \
                    abs(zMin - nextCoord[2]) < boundingBox[2] and \
                    abs(zMax - nextCoord[2]) < boundingBox[2]: #not <= since we include 0
                    if nextCoord not in poly:
                        polyRankUp.append(poly + [nextCoord])

        #print(polyRankUp)
        return polyRankUp

    def getTimePassed(self):
        return time.time() - self.startTime

    def polyListToText(self, polyList):
        pass


enum_polys = Enumerator()

bigList = enum_polys.generateRankWithBounds(7, [3, 3, 3])
print(len(bigList))

'''
pieceDict = {}
for i in range (0, len(bigList)):
    pieceDict[i] = bigList[i]

posDict = {}
for i in range (0, len(bigList)):
    posDict[i] = (0, 0, 5*i)

gui = GUI()
gui.setPiecesAndPos(pieceDict, posDict)
gui.showScreen(fixedColor=True)
'''

#bigList = generateRankWithBounds(10, [5,5])
#print(len(bigList))
#canonical([(-1, 1, 0), (-1, 2, 0), (-2, 2, 0), (-3, 2, 0), (-3, 3, 0), (-3, 3, 1)])
