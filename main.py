from enumerate_polycubes import Enumerator
from assembly import Assembly
from gui import GUI
from piece import Piece

'''
Run everything from this file, should integrate with all other files via class calls
'''

def generatePolycubes(rank, boundingBox=[100, 100, 100]):
    enumerator = Enumerator()
    return enumerator.generateRankWithBounds(rank, boundingBox)

def findAssembies():
    pass

piece1 = Piece([(0, 0, 0), (0, 0, 1), (0, 1, 1)])
piece2 = Piece([(0, 0, 0), (0, 0, 1), (0, 1, 1)])
piece3 = Piece([(0, 0, 0), (0, 0, 1)])
grid = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)]

assembly1 = Assembly([piece1, piece2, piece3], grid)


completeAssemblies = assembly1.assemble()
gui = GUI()
gui.set_mode(mode="assembly", assemblyList=completeAssemblies)
gui.showScreen()


#piece1 = Piece([(0, 0, 0), (0, 0, 1)])
#piece1.determineUniqueRots()
#print(piece1.uniqueRots)