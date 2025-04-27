import tkinter as tk
import sqlite3
from tkinter import messagebox

def open_admin_panel():
    admin_root = tk.Tk()
    admin_root.title("Панель администратора")

    def show_books():
        listbox.delete(0, tk.END)
        conn = sqlite3.connect('bookstore.db')
        cur = conn.cursor()
        cur.execute("SELECT id, title, stock FROM books")
        for row in cur.fetchall():
            listbox.insert(tk.END, f"{row[0]} | {row[1]} | В наличии: {row[2]}")
        conn.close()

    def add_book():
        def save():
            conn = sqlite3.connect('bookstore.db')
            cur = conn.cursor()
            cur.execute("INSERT INTO books (title, author, description, price, stock) VALUES (?, ?, ?, ?, ?)",
                        (title.get(), author.get(), desc.get(), float(price.get()), int(stock.get())))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Книга добавлена")
            add_win.destroy()
            show_books()

        add_win = tk.Toplevel(admin_root)
        add_win.title("Добавить книгу")

        title = tk.StringVar()
        author = tk.StringVar()
        desc = tk.StringVar()
        price = tk.StringVar()
        stock = tk.StringVar()

        for text, var in [("Название", title), ("Автор", author), ("Описание", desc),
                          ("Цена", price), ("Количество", stock)]:
            tk.Label(add_win, text=text).pack()
            tk.Entry(add_win, textvariable=var).pack()

        tk.Button(add_win, text="Сохранить", command=save).pack()

    listbox = tk.Listbox(admin_root, width=80)
    listbox.pack()

    tk.Button(admin_root, text="Обновить список книг", command=show_books).pack()
    tk.Button(admin_root, text="Добавить книгу", command=add_book).pack()

    show_books()
    admin_root.mainloop()
