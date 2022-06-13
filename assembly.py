from subprocess import CompletedProcess
from sympy import Q
from piece import Piece
from gui import GUI

class Assembly():
    def __init__(self, pieces, requiredPositions): #inputs an array of Pieces() and array of required positions

        self.pieceObjects = pieces
        self.piecesWithRotations = []
        self.repeatedPiecesFlag = False

        self.set_pieces(self.pieceObjects)

        self.requiredPositions = requiredPositions

        self.set_canonical_assembly_grid(self.requiredPositions)

        self.fixRequiredPositionsSymmetryProblem()

    def set_pieces(self, pieces = []): #pieces is a 2d array

        pieceHolderArray = []
        for piece in pieces:  #evaluate unique rots
            piece.determineUniqueRots()
            pieceHolderArray.append(piece)
        
        #sort pieces in descending rank and symmetry
        pieceHolderArray = sorted(pieceHolderArray, reverse = True, key = lambda x: (x.getRank(), x.getNumUniqueRotations()))

        self.pieceObjects = pieceHolderArray #sorted

        for piece in pieceHolderArray: #retrieve unique rots
            self.piecesWithRotations.append(piece.getUniqueRotations())

        #check for duplicate pieces
        for i in range (0, len(self.piecesWithRotations)-1): #each group of piece rotations
            for j in range(i+1, len(self.piecesWithRotations)):
                for poly in self.piecesWithRotations[i]:
                    if poly in self.piecesWithRotations[j]:
                        self.repeatedPiecesFlag = True
                        break

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

    def fixRequiredPositionsSymmetryProblem(self):
        '''
        We want to stop solutions where the solution is a rotation of another solution.

        To fix this, I want to find the symmetries of the required positions.

        If I find a rotation that is the same as another, I can restrict the "supplementary" rotation of the first piece in order to stop the solution from happening twice.

        Steps to do this
            1. find all unique rotations of requiredPositions
            2. find supplement of these unique rotations
            3. make those the only allowed rotations for piece1
        '''

        #step 1
        requiredPositionsPiece = Piece(self.requiredPositions)
        requiredPositionsPiece.determineUniqueRots() #find unique rots of required positions
        requiredPositionsUniqueRotations = requiredPositionsPiece.getUniqueRotations()
        
        #step 2:
        requiredPositionsAllRotations = requiredPositionsPiece.getAllCanonicalRots()
        
        uniqueIndexLog = [] #finds index of one occurance of all unique rots
        for uniqueRotation in requiredPositionsUniqueRotations:
            for i in range (0, len(requiredPositionsAllRotations)):
                if requiredPositionsAllRotations[i] == uniqueRotation:
                    uniqueIndexLog.append(i)
                    break
            continue

        #step 3:
        #we need to override self.piecesWithRotations[0]
        #interesting way to do it, notice that every rotation on a cube has order 4 (some have order 2 but that's basically the same thing), so if we just apply the rotation operation of requiredPositionsUniqueRotations three times to piece0, that's the supplemental rotation we're looking for :D

        self.piecesWithRotations[0] = []
        for uniqueIndex in uniqueIndexLog:
            allowedRotation = self.pieceObjects[0].getSupplementaryRot(uniqueIndex)
            self.piecesWithRotations[0].append(allowedRotation)

        print("lengths of pieces with rotations")
        for i in range (0, len(self.piecesWithRotations)):
            print("piece " + str(i) + ": " + str(len(self.piecesWithRotations[i])))

    
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

            #need to figure out how canonical changes allowable positions:
            #because canonicals are sorted by x, y, z, first number in list will return us something in 0z plane

            zeroZCoord = piece[0]
            print("one iteration")
            print(zeroZCoord)

            editedRemainingPositions = remainingPositions.copy()
            x = 0
            while x < len(editedRemainingPositions):
                print(editedRemainingPositions[x])
                editedRemainingPositions[x] = tuple([editedRemainingPositions[x][i]+zeroZCoord[i] for i in range (0, 3)])
                print(editedRemainingPositions[x])
                if editedRemainingPositions[x] not in self.requiredPositions:
                    editedRemainingPositions.pop(x)
                else:
                    x += 1
            
            print(editedRemainingPositions)
 
            for position in editedRemainingPositions: #now we iterate through every position it could be in:
                
                #print("position and remainingPositions")
                #print(position)
                #print(remainingPositions)
                
                positionToMoveTo = tuple([position[i]-zeroZCoord[i] for i in range (0, 3)])
                print(positionToMoveTo)
                pieceInPosition = self.movedPiece(piece, positionToMoveTo) #move piece to that pos

                doesntFit = False #check if piece fits
                for coord in pieceInPosition:
                    if coord not in remainingPositions:
                        doesntFit = True
                        break 

                if doesntFit: #if piece didn't fit
                    #print("didn't fit")
                    continue #skip to next position

                else: #if it did fit:
                    #print("fit")
                    remainingPositionsCopy = remainingPositions.copy() #save copy of remainingPositions
                    for coord in pieceInPosition: #update remaining pieces
                        remainingPositionsCopy.remove(coord)
                    
                    assemblyPath.append((piece, position)) #append this piece to assembly path
                    #print("put piece of index " + str(pieceIndex) + " in")
                    #print("assembly path looking like")
                    #print(assemblyPath)

                    if len(assemblyPath) == numPiecesTotal: #if all pieces put in
                        completeAssemblies.append(assemblyPath.copy()) #add to complete assemblies
                        #print("appending to completeAssemblies")
                        #print(completeAssemblies) #this part works

                    else: #if not all pieces are put in
                        #print("currently going up one level")
                        #print("previous piece has gone in position")
                        #print(position)

                        nextLevelCompleteAssemblies = self.assemble(remainingPositions=remainingPositionsCopy, pieceIndex = pieceIndex+1, assemblyPath = assemblyPath) #do next assembly up

                        for assembly in nextLevelCompleteAssemblies: #append all recursive assemblies

                            completeAssemblies.append(assembly)

                    assemblyPath.pop() #reset assemblyPath

        #extra stuff if pieces are the same in order to remove redundancies
        if pieceIndex == 0:
            if self.repeatedPiecesFlag: #if we've already done everything
                '''
                Note to future Kareem or anyone looking at this:
                This checker removes identical solutions, but doesn't check if
                the rotation of a solution is the same as another solution.
                This would only happen if you used the same piece and a lot 
                of things have to coincidentally work out, so I'm not going to 
                worry about fixing it for now.
                '''
                
                completeAssembliesCopy = completeAssemblies.copy() #need a copy to keep colors in order during display

                for i in range (0, len(completeAssemblies)):
                    completeAssemblies[i] = sorted(completeAssemblies[i], key = lambda x: (x[1][0], x[1][1], x[1][2])) #sort by coord placement
                
                duplicateList = [] #find duplicates
                for i in range (0, len(completeAssemblies)-1):
                    for j in range (i+1, len(completeAssemblies)):
                        if completeAssemblies[i] == completeAssemblies[j]:
                            duplicateList.append((i,j))
                
                for duplicate in duplicateList: #tag duplicates
                    completeAssembliesCopy[duplicate[1]] = None #make the larger number in duplication None
                
                x = 0 #remove duplicates
                while x < len(completeAssembliesCopy):
                    if completeAssembliesCopy[x] == None:
                        completeAssembliesCopy.pop(x) #don't add 1 to x here cause length decreased
                    else:
                        x += 1

                completeAssemblies = completeAssembliesCopy.copy()
                
        return completeAssemblies

