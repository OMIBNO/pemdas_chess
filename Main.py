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
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colors = [p.Color('white'), p.Color('gray')]
    for baris in range(DIMENSI):
        for kolom in range(DIMENSI):
            color = colors[((baris+kolom) % 2)]
            p.draw.rect(screen, color, p.Rect(kolom*SQ_SIZE, baris*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for baris in range(DIMENSI):
        for kolom in range(DIMENSI):
            piece = board[baris][kolom]
            if piece != '--': #ada pion
                #blit untuk menggambar pada screen(memasukkan pion)
                screen.blit(IMAGES[piece], p.Rect(kolom*SQ_SIZE, baris*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()
