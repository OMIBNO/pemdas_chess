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
        IMAGES[piece] = p.image.load('pieces/' + piece + '.png')