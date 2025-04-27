import tkinter as tk
from tkinter import messagebox
import sqlite3
from admin_panel import open_admin_panel

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

root = tk.Tk()
root.title("Вход администратора")

tk.Label(root, text="Логин").pack()
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="Пароль").pack()
entry_password = tk.Entry(root, show='*')
entry_password.pack()

tk.Button(root, text="Войти", command=login).pack()
root.mainloop()
