"""
MAIN MENU UNTUK PROGRAM CATUR
"""

import customtkinter as ctk
import ChessMain

"""
THEME
"""
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

"""
LOGIN
"""
def login():
    global login_nama1, login_password1, login_window
    login_window =ctk.CTk()
    login_window.title('Login')
    login_window.geometry('500x350')
    login_window.resizable(0,0)
    space_empty = ctk.CTkLabel(login_window,
                                         text='')
    space_empty1 = ctk.CTkLabel(login_window,
                                         text='')
    login_nama = ctk.CTkLabel(login_window,
                                           text='Nama',
                                           font=('Arial', 20, 'bold'),
                                           )
    login_nama1 = ctk.CTkEntry(login_window,
                                         placeholder_text='username',
                                         font=('Arial', 15),
                                         width=220,
                                         height=30)
    login_password = ctk.CTkLabel(login_window,
                                            text='Password',
                                            font=('Arial', 20, 'bold'))
    login_password1 = ctk.CTkEntry(login_window,
                                         placeholder_text='password',
                                         font=('Arial', 15),
                                         width=220,
                                         height=30)
    login_button = ctk.CTkButton(login_window,
                                           text='login',
                                           font=('Arial',18),
                                           height=35,
                                           width=80,
                                           command=proses_login)
    login_label = ctk.CTkLabel(login_window,text='USER= kelompok1 PW= chess',
                                        font=('Arial',24,'bold'))
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
        login_window.destroy()
        menu()
    else:
        print('error occured while login')

def menu():
    global app
    app = ctk.CTk()
    app.title('PEMDAS CHESS GAME')
    app.geometry('800x520')
    app.minsize(800, 520)
    app.resizable(True,True)

    s_app = ctk.CTkScrollableFrame(app,
                                        width=800,
                                        height=1000)
    menu_utama_label = ctk.CTkLabel(s_app,text='GAME CHESS KELOMPOK 1',
                                        font=('Arial',43,'bold'))
    s_app.pack(padx=10, pady=10, expand=True, fill='both')
    menu_utama_label.pack()

    ctk.CTkButton(s_app,
              text="PLAY",
              font=('Arial', 20),
              command=lambda: ChessMain.main(),
              width=200,
              height=50,
              border_width=2.9,
              border_color='#0B0C0C',
              corner_radius=10).pack(pady=5)
    ctk.CTkButton(s_app,
              text="EXIT",
              font=('Arial', 20),
              command=lambda: ChessMain.exit(),
              width=200,
              height=50,
              border_width=2.9,
              border_color='#0B0C0C',
              corner_radius=10).pack(pady=5)
    app.mainloop()

def keluar():
    app.destroy()

if __name__ == '__main__':
    login()