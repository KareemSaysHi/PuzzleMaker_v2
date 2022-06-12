from piece import Piece

class Assembly():
    def __init__(self):
        self.piecesWithRotations = []
        self.requiredPositions = []

    def set_pieces(self, pieces = []): #pieces is a 2d array
        if len(pieces) < 2:
            raise ValueError("assembly must have at least two pieces")

        pieceHolderArray = []
        for piece in pieces:  #evaluate unique rots
            pieceHolder = Piece(piece)
            pieceHolder.determineUniqueRots()
            pieceHolderArray.append(pieceHolder)
        
        #sort pieces in descending rank and symmetry
        pieceHolderArray = sorted(pieceHolderArray, reverse = True, key = lambda x: (x.getRank(), x.getNumUniqueRotations()))
            
        for piece in pieceHolderArray: #retrieve unique rots
            self.piecesWithRotations.append(piece.getUniqueRotations())

        #self.piecesWithRotations is now ready

    def set_canonical_assembly_grid(self, requiredPositions):        
        #make required positions canonical:
        
        xCoords = [coord[0] for coord in requiredPositions]
        yCoords = [coord[1] for coord in requiredPositions]
        zCoords = [coord[2] for coord in requiredPositions]

        minX = min(xCoords)
        if minX < 0:
            for i in range (0, len(requiredPositions)):
                requiredPositions[i] = list(requiredPositions[i])
                requiredPositions[i][0] -= minX
                requiredPositions[i] = tuple(requiredPositions[i])
            
        minY = min(yCoords)
        if minY < 0:
            for i in range (0, len(requiredPositions)):
                requiredPositions[i] = list(requiredPositions[i])
                requiredPositions[i][1] -= minY
                requiredPositions[i] = tuple(requiredPositions[i])

        minZ = min(zCoords)
        if minZ < 0:
            for i in range (0, len(requiredPositions)):
                requiredPositions[i] = list(requiredPositions[i])
                requiredPositions[i][2] -= minZ
                requiredPositions[i] = tuple(requiredPositions[i])

        self.requiredPositions = requiredPositions
    
    def movedPiece(self, poly, newPos): #input is a 1D poly array
        movedPoly = poly.copy()
        for i in range (0, len(movedPoly)): #cant just use coord as incrementor cause then you can't edit it 
            movedPoly[i] = list(movedPoly[i])
            movedPoly[i][0] += newPos[0]
            movedPoly[i][1] += newPos[1]
            movedPoly[i][2] += newPos[2]
            movedPoly[i] = tuple(movedPoly[i])
        return movedPoly

    def assemble(self, remainingPositions = None, pieceIndex = 0, assemblyPath = []): 
        if remainingPositions == None: #this means that this is the first piece
            remainingPositions = self.requiredPositions
        
        completeAssemblies = [] #start running list of total assemblies
        #note: assembly path, along with complete assemblies, look like:
        #[(poly array, position), (poly array, position), ...]

        numPiecesTotal = len(self.piecesWithRotations)
        
        #iterate through all of current piece index's rotations 
        for piece in self.piecesWithRotations[pieceIndex]: #each possible rotation
            for position in remainingPositions: #now we iterate through every position it could be in:
                pieceInPosition = self.movedPiece(piece, position) #move piece to that pos

                doesntFit = False #check if piece fits
                for coord in pieceInPosition:
                    if coord not in remainingPositions:
                        doesntFit = True
                        break 

                if doesntFit: #if piece didn't fit
                    continue #skip to next position

                else: #if it did fit:
                    for coord in pieceInPosition: #update remaining pieces
                        remainingPositions.remove(coord)
                    
                    assemblyPath.append((piece, position)) #append this piece to assembly path
                    #print("put piece of index " + str(pieceIndex) + " in")
                    #print("assembly path looking like")
                    #print(assemblyPath)

                    if len(assemblyPath) == numPiecesTotal: #if all pieces put in
                        completeAssemblies.append(assemblyPath.copy()) #add to complete assemblies
                        #print("appending to completeAssemblies")
                        #print(completeAssemblies) #this part works

                    else: #if not all pieces are put in
                        nextLevelCompleteAssemblies = self.assemble(remainingPositions=remainingPositions, pieceIndex = pieceIndex+1, assemblyPath = assemblyPath) #do next assembly up
                        print("next level complete assembly looks like")
                        print(nextLevelCompleteAssemblies)
                        for assembly in nextLevelCompleteAssemblies: #append all recursive assemblies
                            print("WHAT AM I APPENDING")
                            print(assembly)
                            completeAssemblies.append(assembly)

                    for coord in pieceInPosition: #reset remainingPositions
                        remainingPositions.append(coord)

                    assemblyPath.pop() #reset assemblyPath
        
        print("printing complete assemblies at piece index " + str(pieceIndex))
        print (completeAssemblies)
        return completeAssemblies


    #if current piece index = len(self.pieces) - 1:
    #   check and see if remaining piece is a possible omino


