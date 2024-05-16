class GameState():
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bK', 'bQ', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', 'wp', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', 'bp', '--', '--', '--', '--'],
            ['--', '--', 'bp', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wK', 'wQ', 'wB', 'wN', 'wR'],
        ]
        self.moveFunctions = {'p':self.getPawnMoves, 'R':self.getRookMoves, 'N':self.getKnightMoves, 'B':self.getBishopMoves, 'Q':self.getQueenMoves, 'K':self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--' #membuat kotak jadi kosong(karena pion berpindah)
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #dibuat history supaya bisa undo
        self.whiteToMove = not self.whiteToMove #ganti giliran

    def undoMove(self):
        if len(self.moveLog) != 0:#JIKA SUDAH ADA GERAKAN
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #MENGGANTI GILIRAN

    #ALL MOVES CONSIDERING CHECKS
    def getValidMoves(self):
        return self.getAllPossibleMoves()
    
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
        pass
    def getKnightMoves(self, row, col, moves):
        pass
    def getBishopMoves(self, row, col, moves):
        pass
    def getQueenMoves(self, row, col, moves):
        pass
    def getKingMoves(self, row, col, moves):
        pass

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