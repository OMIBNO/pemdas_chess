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
        IMAGES[piece] = p.transform.scale(p.image.load('pieces/' + piece + '.png'), SQ_SIZE, SQ_SIZE)
        #UNTUK MEMANGGIL BISA DENGAN IMAGES['wp]

def main():
    p.init()
    screen = p.display.set_mode((LEBAR, TINGGI))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    GS = ChessEngine.GameState()
    loadimages()
    running = True