import ChessMain
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk
import Game_Main

"""
LOGIN
"""
def login():
    global login_nama1, login_password1, login_window

    login_window = ctk.CTk()
    login_window.title('Login')
    login_window.geometry('500x350')
    login_window.resizable(0, 0)

    # Load the background image
    bg_image = Image.open("img/smktelkomjkt_2.png")
    # Resize the image to a smaller size
    bg_image = bg_image.resize((240, 240), Image.LANCZOS)
    bg_image_tk = ImageTk.PhotoImage(bg_image)

    # Create a label to hold the background image and center it
    bg_label = ctk.CTkLabel(login_window, image=bg_image_tk)
    bg_label.place(relx=0.5, rely=0.5, anchor='center')

    # Overlay your customtkinter widgets on top of the background image
    login_nama = ctk.CTkLabel(login_window, text='Nama', font=('Inter', 20, 'bold'))
    login_nama1 = ctk.CTkEntry(login_window, placeholder_text='username', font=('Inter', 15), width=260, height=30)
    login_password = ctk.CTkLabel(login_window, text='Password', font=('Inter', 20, 'bold'))
    login_password1 = ctk.CTkEntry(login_window, placeholder_text='password', font=('Inter', 15), width=260, height=30, show="*")
    login_button = ctk.CTkButton(login_window, text='login', font=('Inter', 18), height=35, width=80, command=proses_login)
    login_label = ctk.CTkLabel(login_window, text='USER= kelompok1 PW= chess', font=('Inter', 24, 'bold'))

    login_label.pack(pady=10)
    login_nama.pack(pady=5, padx=40, anchor='w')
    login_nama1.pack(pady=5, padx=40, anchor='w')
    login_password.pack(pady=2, padx=40, anchor='w')
    login_password1.pack(pady=2, padx=40, anchor='w') 
    login_button.pack(pady=28)

    login_window.mainloop()

def proses_login():
    username = login_nama1.get()
    password = login_password1.get()
    if username == 'kelompok1' and password == 'chess':
        login_berhasil()
        login_window.after(2000, load_menu)
    else:
        if (username != 'kelompok1' and password == 'chess') or (username == 'kelompok1' and password != 'chess'):
            login_wrong()
        elif (username == '') or (password == ''):
            login_blank()
        else:
            login_wrong()

def load_menu():
    login_window.destroy()
    Game_Main.menu()

def login_berhasil():
    CTkMessagebox(title='Berhasil', message='Anda berhasil login.', icon='check')

def login_wrong():
    CTkMessagebox(title='Gagal', message='User atau password salah.', icon='warning')

def login_blank():
    CTkMessagebox(title='Gagal', message='Ada yang kosong\nMohon isi dengan benar', icon='info')

if __name__ == '__main__':
    login()
