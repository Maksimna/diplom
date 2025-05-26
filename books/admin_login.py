# admin_interface.py

import tkinter as tk
from tkinter import messagebox
import sqlite3
import main  # Чтобы можно было вернуться в главное меню
from admin_panel import open_admin_panel

def admin_login():
    root = tk.Tk()
    root.title("Вход администратора")
    root.minsize(300, 200)  # Чтобы окно было достаточно большим

    def login():
        username = entry_username.get()
        password = entry_password.get()

        conn = sqlite3.connect('bookstore.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM admins WHERE username=? AND password=?", (username, password))
        result = cur.fetchone()
        conn.close()

        if result:
            root.destroy()
            open_admin_panel()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")

    def back_to_main_menu():
        root.destroy()
        main.main_menu()

    # Интерфейс
    tk.Label(root, text="Логин").pack(pady=5)
    entry_username = tk.Entry(root)
    entry_username.pack()

    tk.Label(root, text="Пароль").pack(pady=5)
    entry_password = tk.Entry(root, show='*')
    entry_password.pack()

    # Кнопки
    button_frame = tk.Frame(root)
    button_frame.pack(pady=15)

    tk.Button(button_frame, text="Войти", command=login).pack(side=tk.LEFT, padx=10)

    tk.Button(
        button_frame,
        text="Назад в меню",
        command=back_to_main_menu,
        bg="blue",
        fg="white",
        activebackground="darkblue",
        activeforeground="white",
        font=("Arial", 10, "bold"),
        padx=10,
        pady=2
    ).pack(side=tk.LEFT, padx=10)

    root.mainloop()
