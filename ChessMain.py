"""
File utama
"""
import pygame as p
import ChessEngine

LEBAR = TINGGI = 512
DIMENSI = 8
SQ_SIZE = TINGGI // DIMENSI
MAX_FPS = 15
IMAGES = {}

def loadimages():
    pieces = ['bB', 'bK', 'bN', 'bp', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wp', 'wQ', 'wR']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('pieces/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))
        #UNTUK MEMANGGIL BISA DENGAN IMAGES['wp]

def main():
    p.init()
    screen = p.display.set_mode((LEBAR, TINGGI))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
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
                location = p.mouse.get_pos() #untuk deteksi cursor
                col1 = location[0]//SQ_SIZE
                row1 = location[1]//SQ_SIZE
                if sqSelected == (col1, row1): #klik kotak yg sama 2x
                    sqSelected = () #deselect
                    playerClicks = [] #untuk clear klik
                else:
                    sqSelected = (row1, col1)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    sqSelected = () #reset user click
                    playerClicks = []
            #key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #JIKA Z DIPENCET
                    gs.undoMove()

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colors = [p.Color('white'), p.Color('gray')]
    for row in range(DIMENSI):
        for col in range(DIMENSI):
            color = colors[((row+col) % 2)]
            p.draw.rect(screen, color, p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for row in range(DIMENSI):
        for col in range(DIMENSI):
            piece = board[row][col]
            if piece != '--': #ada pion
                #blit untuk menggambar pada screen(memasukkan pion)
                screen.blit(IMAGES[piece], p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def exit():
    p.quit()

if __name__ == "__main__":
    main()
