from enumerate_polycubes import Enumerator
from assembly import Assembly
from piece import Piece

'''
Run everything from this file, should integrate with all other files via class calls
'''

def generatePolycubes(rank, boundingBox=[100, 100, 100]):
    enumerator = Enumerator()
    return enumerator.generateRankWithBounds(rank, boundingBox)

def findAssembies():
    pass

assembly1 = Assembly()
assembly1.set_pieces([[(0, 0, 0), (0, 0, 1), (0, 1, 1)], [(0, 0, 0), (0, 0, 1), (0, 1, 1)], [(0, 0, 0), (0, 0, 1)]])
assembly1.set_canonical_assembly_grid([(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)]) #2x2x2 square

completeAssemblies = assembly1.assemble()
print(completeAssemblies)

#piece1 = Piece([(0, 0, 0), (0, 0, 1)])
#piece1.determineUniqueRots()
#print(piece1.uniqueRots)