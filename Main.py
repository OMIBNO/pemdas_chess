import pygame
import ChessMain

# Initialize Pygame
pygame.init()

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
kanade_img = pygame.transform.scale(pygame.image.load('img/bg.png'), (800, 520))

# Set up fonts
font_large = pygame.font.Font(None, 43)
font_normal = pygame.font.Font(None, 20)

# Set up the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 520
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('PEMDAS CHESS GAME')

clock = pygame.time.Clock()

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def menu():
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
        pygame.draw.rect(screen, BLUE, play_button_rect)
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

# """
# MAIN MENU UNTUK PROGRAM CATUR

# UKURAN TEXT NORMAL = 18
#             BESAR = 22
# """

# import customtkinter as ctk
# import ChessMain

# """
# THEME
# """
# ctk.set_appearance_mode("Dark")
# ctk.set_default_color_theme("dark-blue")

# """
# LOGIN
# """
# # def login():
# #     global login_nama1, login_password1, login_window
# #     login_window =ctk.CTk()
# #     login_window.title('Login')
# #     login_window.geometry('500x350')
# #     login_window.resizable(0,0)
# #     space_empty = ctk.CTkLabel(login_window,
# #                                          text='')
# #     space_empty1 = ctk.CTkLabel(login_window,
# #                                          text='')
# #     login_nama = ctk.CTkLabel(login_window,
# #                                            text='Nama',
# #                                            font=('Inter', 20, 'bold'),
# #                                            )
# #     login_nama1 = ctk.CTkEntry(login_window,
# #                                          placeholder_text='username',
# #                                          font=('Inter', 15),
# #                                          width=220,
# #                                          height=30)
# #     login_password = ctk.CTkLabel(login_window,
# #                                             text='Password',
# #                                             font=('Inter', 20, 'bold'))
# #     login_password1 = ctk.CTkEntry(login_window,
# #                                          placeholder_text='password',
# #                                          font=('Inter', 15),
# #                                          width=220,
# #                                          height=30)
# #     login_button = ctk.CTkButton(login_window,
# #                                            text='login',
# #                                            font=('Inter',18),
# #                                            height=35,
# #                                            width=80,
# #                                            command=proses_login)
# #     login_label = ctk.CTkLabel(login_window,text='USER= kelompok1 PW= chess',
# #                                         font=('Inter',24,'bold'))
# #     space_empty.pack(pady=6)
# #     login_label.pack()
# #     login_nama.pack(pady=2, padx=141, anchor='w')
# #     login_nama1.pack(pady=5, padx=20)
# #     login_password.pack(pady=2, padx=141, anchor='w')
# #     login_password1.pack(pady=2, padx=20)
# #     login_button.pack(pady=28)
# #     login_window.mainloop()

# # def proses_login():
# #     username = login_nama1.get()
# #     password = login_password1.get()
# #     if username == 'kelompok1' and password == 'chess':
# #         login_window.destroy()
# #         menu()
# #     else:
# #         print('error occured while login')

# def menu():
#     global app
#     app = ctk.CTk()
#     app.title('PEMDAS CHESS GAME')
#     app.geometry('800x520')
#     app.minsize(800, 520)
#     app.resizable(True,True)

#     s_app = ctk.CTkScrollableFrame(app,
#                                         width=800,
#                                         height=1000)
#     menu_utama_label = ctk.CTkLabel(s_app,text='GAME CHESS KELOMPOK 1',
#                                         font=('Inter',43,'bold'))
#     s_app.pack(padx=10, pady=10, expand=True, fill='both')
#     menu_utama_label.pack()

#     #BUTTON PLAY
#     ctk.CTkButton(s_app,
#               text="PLAY",
#               font=('Inter', 20),
#               command=lambda: ChessMain.main(),
#               width=200,
#               height=50,
#               border_width=2.9,
#               border_color='#0B0C0C',
#               corner_radius=10).pack(pady=5)
#     #BUTTON HELP
#     ctk.CTkButton(s_app,
#               text="MANUAL(Help)",
#               font=('Inter', 20),
#               command=lambda: manual(),
#               width=200,
#               height=50,
#               border_width=2.9,
#               border_color='#0B0C0C',
#               corner_radius=10).pack(pady=5)
#     #BUTTON KELUAR CHESSGAME(BUKAN MENU)
#     ctk.CTkButton(s_app,
#               text="EXIT",
#               font=('Inter', 20),
#               command=lambda: ChessMain.exit(),
#               width=200,
#               height=50,
#               border_width=2.9,
#               border_color='#0B0C0C',
#               corner_radius=10).pack(pady=5)
#     app.mainloop()

# def manual():
#     man_text = "HOTKEY"
#     man = ctk.CTkToplevel()
#     man.title('About Us')
#     man.geometry('600x300')
#     man.resizable(0,0)
#     s_man = ctk.CTkScrollableFrame(man,
#                                                     width=558,
#                                                     height=300,
#                                                     )
#     hotkey_label = ctk.CTkLabel(s_man,
#                                             text=man_text,
#                                             text_color='red',
#                                             font=('Inter', 22, 'bold'),
#                                             wraplength=540,
#                                             )
#     s_man.pack(pady=10,padx=5)
#     hotkey_label.pack(anchor='w', padx=10)
#     man.grab_set()

# def keluar():
#     app.destroy()

# if __name__ == '__main__':
#     menu()