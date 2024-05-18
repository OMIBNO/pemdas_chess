import ChessMain
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import time
import Main
"""
LOGIN
"""
def login():
    global login_nama1, login_password1, login_window
    login_window = ctk.CTk()
    login_window.title('Login')
    login_window.geometry('500x350')
    login_window.resizable(0, 0)

    space_empty = ctk.CTkLabel(login_window, text='')
    login_nama = ctk.CTkLabel(login_window, text='Nama', font=('Inter', 20, 'bold'))
    login_nama1 = ctk.CTkEntry(login_window, placeholder_text='username', font=('Inter', 15), width=220, height=30)
    login_password = ctk.CTkLabel(login_window, text='Password', font=('Inter', 20, 'bold'))
    login_password1 = ctk.CTkEntry(login_window, placeholder_text='password', font=('Inter', 15), width=220, height=30, show="*")
    login_button = ctk.CTkButton(login_window, text='login', font=('Inter', 18), height=35, width=80, command=proses_login)
    login_label = ctk.CTkLabel(login_window, text='USER= kelompok1 PW= chess', font=('Inter', 24, 'bold'))

    space_empty.pack(pady=6)
    login_label.pack()
    login_nama.pack(pady=2, padx=141, anchor='w')
    login_nama1.pack(pady=5, padx=20)
    login_password.pack(pady=2, padx=141, anchor='w')
    login_password1.pack(pady=2, padx=20)
    login_button.pack(pady=28)
    
    login_window.mainloop()

def proses_login():
    username = login_nama1.get()
    password = login_password1.get()
    if username == 'kelompok1' and password == 'chess':
        login_berhasil()
        login_window.after(2000, load_menu)
    else:
        #jika SALAH SATU login atau password salah
        if (username != 'kelompok1' and password == 'chess') or (username == 'kelompok1' and password != 'chess'): 
            login_wrong()
        #jika ada yang KOSONG
        elif (username == '') or (password == ''):
            login_blank()
        #jika login username dan password salah
        else:
            login_wrong()

#load menu
def load_menu():
    login_window.destroy()
    Main.menu()

#jika login berhasil(user dan password benar)
def login_berhasil():
    CTkMessagebox(title='Berhasil', message='Anda berhasil login.', icon='check')

#jika login gagal(user atau password salah)
def login_wrong():
    print('here')
    CTkMessagebox(title='Gagal', message='User atau password salah.', icon='warning')

#jika login ada yang kosong
def login_blank():
    CTkMessagebox(title='Gagal', message='Ada yang kosong\nMohon isi dengan benar', icon='info')

if __name__ == '__main__':
    login()


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