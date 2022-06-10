'''
Note: this program is practice in order for me to learn how I'm going to generate polycubes
This program takes an input of rank, and returns all polycubes (no rotation and reflection duplicates)
I got it working! (as of 6/10), confirmed up to rank 8
'''


import numpy as np

monominoes = [[(0, 0)]]
biominoes = [[(0, 0), (1, 0)]]
triominoes = [[(0, 0), (1, 0), (1, 1)], [(0, 0), (1, 0), (2, 0)]]


def generateRank(n):
    '''
    generates all polyominos of rank n
    inputs: rank
    output: 2D list of polyominoes
    '''

    assert n >= 0
    if n == 0:
        return []
    if n == 1:
        return monominoes
    if n == 2:
        return biominoes
    if n == 3:
        return triominoes
    
    polyLastRank = generateRank(n-1)

    #get all next polyominoes
    polyThisRankUnfiltered = []
    for poly in polyLastRank:
        incomingPolys = nextPolyominoes(poly)
        for incomingPoly in incomingPolys:
            polyThisRankUnfiltered.append(incomingPoly)

    #get all rotations and reflections
    polyThisRankRotationsAndReflections = []
    for poly in polyThisRankUnfiltered:
        polyThisRankRotationsAndReflections.append(rotationsAndReflections(poly)) #this is a 3d array
    
    
    polyThisRankCanonical = polyThisRankRotationsAndReflections
    #make everything canonical
    for group in polyThisRankCanonical:
        for i in range (0, len(group)): #need len cause we can't edit poly otherwise
            group[i] = canonical(group[i]) #where group[i] is a poly
            
    #remove redundancies:
    duplicateLog = []
    for i in range(0, len(polyThisRankCanonical)-1): #basically n choose 2 to compare all possibilities
        for j in range(i+1, len(polyThisRankCanonical)): #note again that polyThisRankCanonical is 3D
            if not isUnique(polyThisRankCanonical[i], polyThisRankCanonical[j]):
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
    return polyThisRankFinal

def isUnique(polyGroup1, polyGroup2): #tested and works
    '''
    Takes in two polyGroups (rots and reflections), and sees if they are the same
    Inputs: Two 2D array poly groups
    Outputs: bool True or Falses
    '''

    for poly in polyGroup1:
        if poly in polyGroup2:
            return False

    return True

rot90 = lambda x, y: (-y, x)
rot180 = lambda x, y: (-x, -y)
rot270 = lambda x, y: (y, -x)
reflect = lambda x, y: (-x, y)

def rotationsAndReflections(poly): #tested and works

    xCoords = [coord[0] for coord in poly]
    yCoords = [coord[1] for coord in poly]

    rotationsAndReflectionsList = [
        poly,
        list(map(rot90, xCoords, yCoords)),
        list(map(rot180, xCoords, yCoords)),
        list(map(rot270, xCoords, yCoords)),
        list(map(reflect, xCoords, yCoords)),
        [reflect(rot90(coord[0], coord[1])[0], rot90(coord[0], coord[1])[1]) for coord in poly],
        [reflect(rot180(coord[0], coord[1])[0], rot180(coord[0], coord[1])[1]) for coord in poly],
        [reflect(rot270(coord[0], coord[1])[0], rot270(coord[0], coord[1])[1]) for coord in poly],
    ]

    #print(rotationsAndReflectionsList)
    return(rotationsAndReflectionsList)

def canonical(poly): #tested and works
    '''
    sorts and brings polyominoes to origin
    Inputs: 1D array with polyomino coords
    Outputs: corrected polyomino
    '''

    poly = sorted(poly, key = lambda x: (x[0], x[1])) #sort by x first, then y
    
    xCoords = [coord[0] for coord in poly]
    yCoords = [coord[1] for coord in poly]

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

    #print(poly)
    return poly

def nextPolyominoes(poly): #tested and works
    '''
    Given a polyomino of rank n, returns all possible extensions of the polyomino with rank n+1
    Inputs: 1D array with polyomino coords
    Output: list of polyominoes 
    '''
    newSquare = lambda x, y: [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

    xCoords = [coord[0] for coord in poly]
    yCoords = [coord[1] for coord in poly]

    newSquares = list(map(newSquare, xCoords, yCoords)) #2d array
    
    polyRankUp = []
    for neighborhood in newSquares:
        for nextCoord in neighborhood:
            if nextCoord not in poly:
                polyRankUp.append(poly + [nextCoord])

    #print(polyRankUp)
    return polyRankUp

bigList = generateRank(8)
print(len(bigList))
#canonical([(-1, 1), (-1, 2), (-2, 2), (-3, 2), (-3, 3)])
#rotationsAndReflections([(0, 0), (0, 1), (0, 2), (1, 2)])



