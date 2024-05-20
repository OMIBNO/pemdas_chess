import ChessMain

class GameState():
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]
        self.moveFunctions = {
            'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 
            'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves
        }
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = ()
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'  # Remove the piece from the starting square
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # Log the move
        self.whiteToMove = not self.whiteToMove  # Switch turns
        # Update the king's location if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        # PAWN PROMOTION
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'
        
        #En passant move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--' #capturing the pawn note= pake board[startrow][endcol] karena pawn lawan di row yang sama, tapi di col yang beda

        #update enpassant move variable
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: #only on 2 square pawn advances
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()

        #castle move
        if move.isCastleMove:
            if move.endCol- move.startCol == 2: #king side castle move
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1] #moves the rock
                self.board[move.endRow][move.endCol+1] = '--' #erase old rook
            else: #queenside castle move
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2] #moves the rock
                self.board[move.endRow][move.endCol-2] = '--' #erase old rook

        #update castling rights - whenever it is a rook or a king move
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))

    def undoMove(self):
        if len(self.moveLog) != 0:  # If there's a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # Switch turns back
            # Update the king's location if needed
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            #undo enpassant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--' #leave landing square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            #undo a 2 square advances
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endCol) == 2:
                self.enpassantPossible = ()
            #undo castling rights
            self.castleRightsLog.pop() #get rid of the new castle rights from the move we are undoing
            self.currentCastlingRight = self.castleRightsLog[-1] #set the current castle rights to the last one on the list
            #undo castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2: #king side
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = '--'
                else: #queen side
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = '--'

    #UPDATE THE CASTLE RIGHTS GIVEN THE MOVE
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0: #left rook
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7: #right rook
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0: #left rook
                    self.currentCastlingRight.bqs = False
                if move.startCol == 7: #right rook
                    self.currentCastlingRight.bks = False



    # All moves considering checks
    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                        self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        moves = self.getAllPossibleMoves()  # 1. Generate all possible moves
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        for i in range(len(moves) - 1, -1, -1):  # When removing from a list, go backwards through the list
            self.makeMove(moves[i])  # 2. Make the move
            self.whiteToMove = not self.whiteToMove  # 3. Switch turns
            if self.inCheck():  # 4. Check if the move puts the king in check
                moves.remove(moves[i])  # 5. If so, it's not a valid move
            self.whiteToMove = not self.whiteToMove  # Switch turns back
            self.undoMove()
        if len(moves) == 0:  # Either checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastleRights
        return moves

    # Determine if the player in move is in check
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    # Determine if the enemy can attack the square row, col
    def squareUnderAttack(self, row, col):
        self.whiteToMove = not self.whiteToMove  # Switch to opponent's turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove  # Switch turns back
        for move in oppMoves:
            if move.endRow == row and move.endCol == col:  # Square is under attack
                return True
        return False

    # All moves without considering checks
    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]
                    self.moveFunctions[piece](row, col, moves)
        return moves

    """
    GET PAWN MOVES
    """
    def getPawnMoves(self, row, col, moves):
        if self.whiteToMove:  # For white pawns
            if self.board[row - 1][col] == '--':  # 1 square advance
                moves.append(Move((row, col), (row - 1, col), self.board))
                if row == 6 and self.board[row - 2][col] == '--':  # 2 square advance
                    moves.append(Move((row, col), (row - 2, col), self.board))
            if col - 1 >= 0:  # Capture to the left
                if self.board[row - 1][col - 1][0] == 'b':  # Enemy piece to capture
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))
                elif (row - 1, col - 1) == self.enpassantPossible:
                    moves.append(Move((row, col), (row - 1, col - 1), self.board, isEnpassantMove=True))
            if col + 1 <= 7:  # Capture to the right
                if self.board[row - 1][col + 1][0] == 'b':  # Enemy piece to capture
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))
                elif (row - 1, col + 1) == self.enpassantPossible:
                    moves.append(Move((row, col), (row - 1, col + 1), self.board, isEnpassantMove=True))
        
        else:  # For black pawns
            if self.board[row + 1][col] == '--':  # 1 square advance
                moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == '--':  # 2 square advance
                    moves.append(Move((row, col), (row + 2, col), self.board))
            if col - 1 >= 0:  # Capture to the left
                if self.board[row + 1][col - 1][0] == 'w':  # Enemy piece to capture
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
                elif (row + 1, col - 1) == self.enpassantPossible:
                    moves.append(Move((row, col), (row + 1, col - 1), self.board, isEnpassantMove=True))
            if col + 1 <= 7:  # Capture to the right
                if self.board[row + 1][col + 1][0] == 'w':  # Enemy piece to capture
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))
                elif (row + 1, col + 1) == self.enpassantPossible:
                    moves.append(Move((row, col), (row + 1, col + 1), self.board, isEnpassantMove=True))

    """
    GET ROOK MOVES
    """
    def getRookMoves(self, row, col, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # Up, left, down, right
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # On board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':  # Empty space is valid
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # Enemy piece is valid
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:  # Friendly piece is invalid
                        break
                else:  # Off board
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
                if endPiece[0] != allyColor:  # Not an ally piece (empty or enemy piece)
                    moves.append(Move((row, col), (endRow, endCol), self.board))

    """
    GET BISHOP MOVES
    """
    def getBishopMoves(self, row, col, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # 4 diagonals
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):  # Bishop can move max of 7 squares
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # Is it on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':  # Empty space is valid
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # Enemy piece is valid
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:  # Friendly piece is invalid
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
                if endPiece[0] != allyColor:  # Not an ally piece (empty or enemy piece)
                    moves.append(Move((row, col), (endRow, endCol), self.board))

    """
    GENERATE ALL VALID CASTLE MOVES FOR THE KING AT(ROW, COL) AND ADD THEM TO THE LIST OF MOVES
    """
    def getCastleMoves(self, row, col, moves):
        if self.squareUnderAttack(row, col):
            return #can't castle while in check
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingSideCastleMoves(row, col, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueenSideCastleMoves(row, col, moves)
        
    def getKingSideCastleMoves(self, row ,col, moves):
        if self.board[row][col+1] == '--' and self.board[row][col+2] == '--':
            if not self.squareUnderAttack(row, col+1) and not self.squareUnderAttack(row, col+2):
                moves.append(Move((row, col), (row, col+2), self.board, isCastleMove=True))

    def getQueenSideCastleMoves(self, row ,col, moves):
        if self.board[row][col-1] == '--' and self.board[row][col-2] == '--' and self.board[row][col-3] == '--':
            if not self.squareUnderAttack(row, col-1) and not self.squareUnderAttack(row, col-2):
                moves.append(Move((row, col), (row, col-2), self.board, isCastleMove=True))

#TO HANDLE CASTLING MOVE
class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move():
    # Maps keys to values
    ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)
        #en passant
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
        #castle move
        self.isCastleMove = isCastleMove
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)

    # Overriding the equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]

if __name__ == '__main__':
    ChessMain.main()