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

    loadimages()
    running = True
    sqSelected = () #untuk mengetahui klik terbaru
    playerClicks = [] #untuk mengetahui clicks, seperti click history
    p.event.get()

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
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
                                sqSelected = ()  # Reset user clicks
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # Undo move
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        drawSidebar(screen, gs)  # Draw the sidebar
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
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

def exit():
    p.quit()

if __name__ == "__main__":
    main()
