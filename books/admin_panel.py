import tkinter as tk
import sqlite3
from tkinter import messagebox

def open_admin_panel():
    admin_root = tk.Tk()
    admin_root.title("Панель администратора")
    admin_root.configure(bg="lightgray")

    def show_books():
        listbox.delete(0, tk.END)
        conn = sqlite3.connect('bookstore.db')
        cur = conn.cursor()
        # Правильные названия столбцов: stock_quantity вместо stock
        cur.execute("SELECT id, title, stock_quantity FROM books")
        for row in cur.fetchall():
            listbox.insert(tk.END, f"{row[0]} | {row[1]} | В наличии: {row[2]}")
        conn.close()

    def add_book():
        def save():
            try:
                # Конвертируем год, purchase_price и sale_price в нужные типы
                year_int = int(year.get()) if year.get() else None
                purchase_price_float = float(purchase_price.get()) if purchase_price.get() else None
                sale_price_float = float(sale_price.get()) if sale_price.get() else None
                stock_int = int(stock.get()) if stock.get() else 0

                conn = sqlite3.connect('bookstore.db')
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO books (title, author, genre, publisher, year, isbn, purchase_price, sale_price, stock_quantity, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    title.get(), author.get(), genre.get(), publisher.get(), year_int, isbn.get(),
                    purchase_price_float, sale_price_float, stock_int, description.get()
                ))
                conn.commit()
                conn.close()
                messagebox.showinfo("Успех", "Книга добавлена")
                add_win.destroy()
                show_books()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить книгу:\n{e}")

        add_win = tk.Toplevel(admin_root)
        add_win.title("Добавить книгу")

        title = tk.StringVar()
        author = tk.StringVar()
        genre = tk.StringVar()
        publisher = tk.StringVar()
        year = tk.StringVar()
        isbn = tk.StringVar()
        purchase_price = tk.StringVar()
        sale_price = tk.StringVar()
        stock = tk.StringVar()
        description = tk.StringVar()

        fields = [
            ("Название", title),
            ("Автор", author),
            ("Жанр", genre),
            ("Издательство", publisher),
            ("Год издания", year),
            ("ISBN", isbn),
            ("Закупочная цена", purchase_price),
            ("Цена продажи", sale_price),
            ("Количество на складе", stock),
            ("Описание", description)
        ]

        for text, var in fields:
            tk.Label(add_win, text=text).pack()
            tk.Entry(add_win, textvariable=var).pack()

        tk.Button(add_win, text="Сохранить", command=save).pack()

    listbox = tk.Listbox(admin_root, width=100)
    listbox.pack()

    tk.Button(admin_root, text="Обновить список книг", command=show_books).pack()
    tk.Button(admin_root, text="Добавить книгу", command=add_book).pack()

    show_books()
    admin_root.mainloop()
