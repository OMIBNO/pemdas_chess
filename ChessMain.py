import pygame as p
import ChessEngine

LEBAR = 800 
TINGGI = 512
DIMENSI = 8
SQ_SIZE = TINGGI // DIMENSI
MAX_FPS = 15
IMAGES = {}
SIDEBAR_WIDTH = LEBAR - TINGGI

def loadimages():
    pieces = ['bB', 'bK', 'bN', 'bp', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wp', 'wQ', 'wR']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('pieces/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((LEBAR, TINGGI))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False
    loadimages()
    running = True
    sqSelected = () #untuk mengetahui klik terbaru
    playerClicks = [] #untuk mengetahui clicks, seperti click history
    gameOver = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if col < DIMENSI:  # Ensure the click is within the board area
                        if sqSelected == (row, col):
                            sqSelected = ()  # Deselect
                            playerClicks = []  # Clear clicks
                        else:
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected)
                        if len(playerClicks) == 2: #after second click
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            print(move.getChessNotation())
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gs.makeMove(validMoves[i])
                                    moveMade = True
                                    animate = True
                                    sqSelected = ()  # Reset user clicks
                                    playerClicks = []
                            if not moveMade:
                                playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # Undo move
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r: #reset board
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            gs.getValidMoves()
            moveMade = False
            animat = False

        drawGameState(screen, gs, validMoves, sqSelected)
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')    
        drawSidebar(screen, gs)  # Draw the sidebar
        clock.tick(MAX_FPS)
        p.display.flip()

"""
Highlight square selected and moves for place selected
"""
def highlightSquare(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        row, col = sqSelected
        if gs.board[row][col][0] == ('w' if gs.whiteToMove else 'b'): #sqSelected is a piece that can be moved
            #hightlight sqSelected
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) #transparency, (0 = transparent, 255 = opaque)
            s.fill(p.Color('blue'))
            screen.blit(s, (col*SQ_SIZE, row*SQ_SIZE))
            #highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == row and move.startCol == col:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

def drawGameState(screen, gs, validMoves, sqSelected):
    global colors
    drawBoard(screen)
    highlightSquare(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    global colors
    colors = [p.Color('white'), p.Color('gray')]
    for row in range(DIMENSI):
        for col in range(DIMENSI):
            color = colors[((row + col) % 2)]
            p.draw.rect(screen, color, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for row in range(DIMENSI):
        for col in range(DIMENSI):
            piece = board[row][col]
            if piece != '--':  # There is a piece
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawSidebar(screen, gs):
    sidebar_rect = p.Rect(TINGGI, 0, SIDEBAR_WIDTH, TINGGI)
    p.draw.rect(screen, p.Color('lightgreen'), sidebar_rect)

    # Set up fonts
    font = p.font.SysFont('Inter', 24)
    small_font = p.font.SysFont('Inter', 20)

    # Display whose turn it is
    turn_text = 'White' if gs.whiteToMove else 'Black'
    text_surface = font.render('Turn: ' + turn_text, True, p.Color('black'))
    screen.blit(text_surface, (TINGGI + 10, 10))

    # Display move history
    move_y = 50
    for i in range(0, len(gs.moveLog), 2):
        # Display the move number
        move_number_surface = small_font.render(f"{(i//2) + 1}.", True, p.Color('black'))
        screen.blit(move_number_surface, (TINGGI + 10, move_y))
        
        if i < len(gs.moveLog):
            # Display White's move
            white_move_surface = small_font.render(gs.moveLog[i].getChessNotation(), True, p.Color('white'))
            screen.blit(white_move_surface, (TINGGI + 50, move_y))
        
        if i + 1 < len(gs.moveLog):
            # Display Black's move
            black_move_surface = small_font.render(gs.moveLog[i + 1].getChessNotation(), True, p.Color('black'))
            screen.blit(black_move_surface, (TINGGI + 150, move_y))

        """
        sistem checkmate/stale nanti terapkan terpisah dari drawsidebar
        """
        # if gs.checkMate == True:
        #     isCheck = font.render('Checkmate', True, p.Color('black'))
        #     screen.blit(isCheck, (TINGGI + 20, 20))

        move_y += 30

"""
ANIMATING A MOVE
"""
def animateMove(move, screen, board, clock):
    global colors
    coords = [] #list of coords that the animation will move through
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 #frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        row, col = ((move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount))
        drawBoard(screen)
        drawPieces(screen, board)
        #erase the piece moved from its ending squares
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #draw captured piece onto rectangles
        if move.pieceCaptured != '--':
            screen.blit (IMAGES[move.pieceCaptured], endSquare)
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(120)

def drawText(screen, text):
    font = p.font.SysFont('Inter', 32, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0, 0, 512, TINGGI).move(512/2 - textObject.get_width()/2, TINGGI/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))

def exit():
    p.quit()

if __name__ == "__main__":
    main()
