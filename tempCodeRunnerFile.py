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
            
            # Undo en passant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--'  # Leave landing square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured  # Restore the captured pawn
                self.enpassantPossible = (move.endRow, move.endCol) if self.whiteToMove else (move.startRow, move.endCol)
            elif move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()
            
            # Restore castling rights
            self.castleRightsLog.pop()  # Remove the latest castle rights update
            self.currentCastlingRight = self.castleRightsLog[-1]  # Restore the previous castling rights
            
            # Undo castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:  # King side
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '--'
                else:  # Queen side
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'