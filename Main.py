import pygame
import ChessMain
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import time

# Initialize Pygame
pygame.init()

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
kanade_img = pygame.transform.scale(pygame.image.load('img/bg.png'), (800, 520))

# Set up fonts
font_large = pygame.font.Font(None, 43)
font_normal = pygame.font.Font(None, 22)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
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
                if play_button_rect.collidepoint(event.pos):
                    ChessMain.main()
                elif help_button_rect.collidepoint(event.pos):
                    manual()
                elif exit_button_rect.collidepoint(event.pos):
                    keluar()

        # Blit the background image
        screen.blit(kanade_img, (0, 0))

        # Draw main menu label
        draw_text("GAME CHESS KELOMPOK 1", font_large, WHITE, SCREEN_WIDTH // 2, 100)

        # Draw buttons
        button_width = 200
        button_height = 50
        button_spacing = 70
        play_button_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, 200, button_width, button_height)
        pygame.draw.rect(screen, BLACK, play_button_rect)
        draw_text("PLAY", font_normal, WHITE, play_button_rect.centerx, play_button_rect.centery)

        help_button_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, 200 + button_spacing, button_width, button_height)
        pygame.draw.rect(screen, BLUE, help_button_rect)
        draw_text("MANUAL(Help)", font_normal, WHITE, help_button_rect.centerx, help_button_rect.centery)

        exit_button_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, 200 + 2 * button_spacing, button_width, button_height)
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
        draw_text(man_text, font_normal, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        pygame.display.flip()
        clock.tick(60)

def keluar():
    pygame.quit()

if __name__ == '__main__':
    menu()
