class GameState():
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bK', 'bQ', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wK', 'wQ', 'wB', 'wN', 'wR'],
        ]
        self.moveFunctions = {'p':self.getPawnMoves, 'R':self.getRookMoves, 'N':self.getKnightMoves, 'B':self.getBishopMoves, 'Q':self.getQueenMoves, 'K':self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 3)
        self.blackKingLocation = (0, 3)

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--' #membuat kotak jadi kosong(karena pion berpindah)
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #dibuat history supaya bisa undo
        self.whiteToMove = not self.whiteToMove #ganti giliran
        #update lokasi king
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

    def undoMove(self):
        if len(self.moveLog) != 0:#JIKA SUDAH ADA GERAKAN
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #MENGGANTI GILIRAN
            #update lokasi king if needed
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

    #ALL MOVES CONSIDERING CHECKS
    def getValidMoves(self):
        #1. Generate all possible moves
        moves = self.getAllPossibleMoves()
        #2. For each move, make the move
        for i in range(len(moves)-1, -1, -1): #when removing from a list go backwards through that list
            self.makeMove(moves[i])
            #3. Generate all opponent's move
            #4. For each of your opponent's moves, see if they attack your king
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])#5. If they do attack your king, it's not a valid move
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        return moves

    #DETERMINE IF THE PLAYER IN MOVE IS IN CHECK
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    #DETERMINE IF THE ENEMY CAN ATTACK THE SQUARE ROW, COL
    def squareUnderAttack(self, row, col):
        self.whiteToMove = not self.whiteToMove #switch to opponents turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove #switch turns back
        for move in oppMoves:
            if move.endRow == row and move.endCol == col: #square is under attack
                return True
        return False


    #ALL MOVES WITHOUT CONSIDERING CHECKS
    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]
                    print(self.whiteToMove)
                    self.moveFunctions[piece](row, col, moves)
        return moves

    """
    GET PAWN MOVES
    """
    def getPawnMoves(self, row, col, moves):
        if self.whiteToMove: #For white pawn
            if self.board[row-1][col] == '--': #Pawn, 1 square advance, to blank square
                moves.append(Move((row, col), (row-1, col), self.board))
                if row == 6 and self.board[row-2][col] == '--': #2 square advance
                    moves.append(Move((row,col), (row-2, col), self.board)) 
            if col-1 >= 0: #Capture to the left
                if self.board[row-1][col-1][0] == 'b': #black pawn
                    moves.append(Move((row, col), (row-1, col-1), self.board))
            if col+1 <= 7: #Capture to the right
                if self.board[row-1][col+1][0] == 'b': #black pawn
                    moves.append(Move((row, col), (row-1, col+1), self.board))
        else: #For black pawn
            if self.board[row+1][col] == '--':#1 square advance
                moves.append(Move((row, col), (row+1, col), self.board))
                if row == 1 and self.board[row+2][col] == '--':#2 square advance
                    moves.append(Move((row, col), (row+2, col), self.board))
            if col-1 >= 0:#Capture to the left
                if self.board[row+1][col-1][0] == 'w':#white pawn
                    moves.append(Move((row, col), (row+1, col-1), self.board))
            if col+1 <= 7:#Capture to the right
                if self.board[row+1][col+1][0] == 'w':#white pawn
                    moves.append(Move((row, col), (row+1, col+1), self.board))

    """
    GET ROOK MOVES
    """
    def getRookMoves(self, row, col, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) #up, left, down, right
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--': # empty space valid
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #enemy piece valid
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else: # friendly piece invalid
                        break
                else: #off board
                    break

    
    """
    GET KNIGHT MOVES
    """
    def getKnightMoves(self, row, col, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = row + m[0]
            endCol = col + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #not an ally piece(empty or enemy piece)
                    moves.append(Move((row, col), (endRow, endCol), self.board))
    
    """
    GET BISHOP MOVES
    """
    def getBishopMoves(self, row, col, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) #4 diagonal
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8): #bishop can move max of 7 squares
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #is it on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--': #empty space valid
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #enemy piece valid
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else: #friendly piece invalid
                        break
                else:
                    break

    """
    GET QUEEN MOVES
    """
    def getQueenMoves(self, row, col, moves):
        self.getRookMoves(row, col, moves)
        self.getBishopMoves(row, col, moves)

    """
    GET KING MOVES
    """
    def getKingMoves(self, row, col, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = row + kingMoves[i][0]
            endCol = col + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #not an ally piece( empyty or enemy piece)
                    moves.append(Move((row, col), (endRow, endCol), self.board))



class Move():
# maps keys to values
# key : value
    ranksToRows = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)

    """
    OVERRIDING THE EQUALS METHOD
    """
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]