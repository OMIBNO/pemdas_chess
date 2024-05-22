import pygame
import ChessMain, ChessMain_2
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import time

# Initialize Pygame
pygame.init()

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
fill_img = pygame.transform.scale(pygame.image.load('img/white_bg.jpg'), (800, 520))
bg_img = pygame.transform.scale(pygame.image.load('img/smktelkomjkt_2.png'), (300, 300))

# Set up fonts
font_large = pygame.font.SysFont('Monospace', 43)
font_normal = pygame.font.SysFont('Monospace', 22)
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_text_left(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)  # Set the top left corner to the specified coordinates
    screen.blit(text_surface, text_rect)


def menu():
    # Set up the screen
    global SCREEN_WIDTH, SCREEN_HEIGHT
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 520
    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('PEMDAS CHESS GAME')
    global clock
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button1_rect.collidepoint(event.pos):
                    ChessMain.main()
                elif play_button2_rect.collidepoint(event.pos):
                    ChessMain_2.main()
                elif help_button_rect.collidepoint(event.pos):
                    manual()
                elif exit_button_rect.collidepoint(event.pos):
                    keluar()

        # Blit the background image
        screen.blit(fill_img, (0, 0))
        screen.blit(bg_img, (230, 130))

        # Draw main menu label
        draw_text("GAME CHESS KELOMPOK 1", font_large, BLACK, SCREEN_WIDTH // 2, 100)

        # Draw buttons
        button_width = 400
        button_height = 50
        button_spacing = 70
        play_button1_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, 200, button_width, button_height)
        pygame.draw.rect(screen, BLACK, play_button1_rect)
        draw_text("PLAY(Single Player)", font_normal, WHITE, play_button1_rect.centerx, play_button1_rect.centery)

        play_button2_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, 200 + button_spacing, button_width, button_height)
        pygame.draw.rect(screen, BLACK, play_button2_rect)
        draw_text("PLAY(Multi Player)", font_normal, WHITE, play_button2_rect.centerx, play_button2_rect.centery)

        help_button_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, 200 + 2 * button_spacing, button_width, button_height)
        pygame.draw.rect(screen, BLUE, help_button_rect)
        draw_text("MANUAL(Help)", font_normal, WHITE, help_button_rect.centerx, help_button_rect.centery)

        exit_button_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, 200 + 3 * button_spacing, button_width, button_height)
        pygame.draw.rect(screen, BLUE, exit_button_rect)
        draw_text("EXIT", font_normal, WHITE, exit_button_rect.centerx, exit_button_rect.centery)

        pygame.display.flip()
        clock.tick(60)

def manual():
    man_text = "HOTKEY"
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        # Informasi hotkey
        draw_text_left(man_text, font_large, BLUE, 0, 0)
        draw_text_left('Undo Move    = Z', font_normal, WHITE, 0, 45)
        draw_text_left('Restart Game = R', font_normal, WHITE, 0, 70)

        # Informasi kelompok
        draw_text_left('ANGGOTA KELOMPOK', font_large, BLUE, 340, 0)
        draw_text_left('1. Raihan Wiraseno Putra', font_normal, WHITE, 340, 45)
        draw_text_left('2. Malvin Gunawan', font_normal, WHITE, 340, 70)
        draw_text_left('3. Vinza Nur Akmal', font_normal, WHITE, 340, 95)
        draw_text_left('4. Sabrina Azzahra', font_normal, WHITE, 340, 120)
        draw_text_left('5. La Ode Aditya Rahman', font_normal, WHITE, 340, 145)
        pygame.display.flip()
        clock.tick(60)

def keluar():
    pygame.quit()

if __name__ == '__main__':
    menu()
