import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox
from datetime import datetime


def admin_login():
    def login():
        if entry_code.get() == "admin123":
            login_win.destroy()
            open_admin_panel()
        else:
            messagebox.showerror("Ошибка", "Неверный код администратора")

    login_win = tk.Tk()
    login_win.title("Вход администратора")
    login_win.configure(bg="grey")

    tk.Label(login_win, text="Введите код администратора:").pack(pady=5)
    entry_code = tk.Entry(login_win, show="*")
    entry_code.pack(pady=5)
    tk.Button(login_win, text="Войти", command=login).pack(pady=5)
    def back_to_main_menu():
        import main  # импорт внутри функции
        login_win.destroy()
        main.main_menu()
    button_frame = tk.Frame(login_win)  # Создаем контейнер для кнопок
    button_frame.pack(fill=tk.X)  # Контейнер растягивается на всю ширину окна
    back_to_menu_button = tk.Button(
        button_frame,
        text="В главное меню",
        command=back_to_main_menu,
        bg="blue",
        fg="white",
        activebackground="darkblue",
        activeforeground="white",
        font=("Arial", 10, "bold"),
        padx=10,
        pady=2
    )
    back_to_menu_button.pack(padx=5, pady=5)
    login_win.mainloop()

def cashier_login():
    def login():
        email = entry_email.get()
        password = entry_password.get()

        conn = sqlite3.connect("bookstore.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND password=? AND role='Кассир'", (email, password))
        user = cur.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Успех", "Вход выполнен как кассир")
            login_win.destroy()
            open_admin_panel()
        else:
            messagebox.showerror("Ошибка", "Неверный email или пароль, либо вы не кассир")

    def back_to_main_menu():
        import main
        login_win.destroy()
        main.main_menu()

    login_win = tk.Tk()
    login_win.title("Вход кассира")
    login_win.configure(bg="#ccffcc")  # Светло-зеленый фон

    tk.Label(login_win, text="Email кассира:", bg="#ccffcc").pack(pady=5)
    entry_email = tk.Entry(login_win)
    entry_email.pack(pady=5)

    tk.Label(login_win, text="Пароль:", bg="#ccffcc").pack(pady=5)
    entry_password = tk.Entry(login_win, show="*")
    entry_password.pack(pady=5)

    tk.Button(login_win, text="Войти", command=login).pack(pady=5)

    button_frame = tk.Frame(login_win, bg="#ccffcc")
    button_frame.pack(fill=tk.X)

    back_to_menu_button = tk.Button(
        button_frame,
        text="В главное меню",
        command=back_to_main_menu,
        bg="green",
        fg="white",
        activebackground="darkgreen",
        activeforeground="white",
        font=("Arial", 10, "bold"),
        padx=10,
        pady=2
    )
    back_to_menu_button.pack(padx=5, pady=5)

    login_win.mainloop()

def open_admin_panel():

    admin_root = tk.Tk()
    admin_root.title("Панель администратора")
    admin_root.configure(bg="grey")

    conn = sqlite3.connect('bookstore.db')
    cur = conn.cursor()



    conn.commit()

    # === Создаем общий фрейм для вкладок и кнопки выхода ===
    top_frame = tk.Frame(admin_root)
    top_frame.pack(fill="x")  # растянуть по ширине

    # === Создаем вкладки ===
    tab_control = ttk.Notebook(top_frame)
    top_frame.configure(bg="grey")

    # Вкладка "Главная"
    tab_main = ttk.Frame(tab_control)
    tab_control.add(tab_main, text="Главная")

    # Вкладка "Продажи"
    tab_sales = ttk.Frame(tab_control)
    tab_control.add(tab_sales, text="Продажи")
    # Вкладка "Закупки"
    tab_purchases = ttk.Frame(tab_control)
    tab_control.add(tab_purchases, text="Закупки")

    # Вкладка "Пользователи"
    tab_stores = ttk.Frame(tab_control)
    tab_control.add(tab_stores, text="Пользователи")

    # Вкладка "Покупки"
    tab_finances = ttk.Frame(tab_control)
    tab_control.add(tab_finances, text="Покупки")

    # Вкладка "Корзина"
    tab_crm = ttk.Frame(tab_control)
    tab_control.add(tab_crm, text="Корзина")

    # Вкладка "Избранное"
    tab_company = ttk.Frame(tab_control)
    tab_control.add(tab_company, text="Избранное")

    # Вкладка "О компании"
    tab_references = ttk.Frame(tab_control)
    tab_control.add(tab_references, text="О компании")

    # Вкладка "О компании"
    tab_reports = ttk.Frame(tab_control)
    tab_control.add(tab_reports, text = "Отчеты и аналитика")


    tab_control.pack(side=tk.LEFT, fill="x", expand=True)  # вкладки влево, растягиваются

    def back_to_main_menu():
        import main  # импорт внутри функции
        admin_root.destroy()
        main.main_menu()

        # Элементы интерфейса

    button_frame = tk.Frame(admin_root)  # Создаем контейнер для кнопок
    button_frame.configure(bg="grey")
    button_frame.pack(fill=tk.X)  # Контейнер растягивается на всю ширину окна
    back_to_menu_button = tk.Button(
        button_frame,
        text="В главное меню",
        command=back_to_main_menu,
        bg="blue",
        fg="white",
        activebackground="darkblue",
        activeforeground="white",
        font=("Arial", 10, "bold"),
        padx = 10,
        pady = 2
    )
    back_to_menu_button.pack(padx=5, pady=5)


    # === Кнопка Выход рядом с вкладками ===
    exit_button = tk.Button(
        top_frame,
        text="Выход",
        command=admin_root.destroy,
        bg="red",
        fg="white",
        activebackground="darkred",
        activeforeground="white",
        font=("Arial", 10, "bold"),
        padx=10,
        pady=2
    )
    exit_button.pack(padx=5, pady=5)  # ставим её тоже слева, рядом с вкладками


    def show_users():
        # Очистка listbox перед добавлением новых данных
        if listbox3:
            listbox3.delete(0, tk.END)

        # Подключаемся к базе данных
        conn = sqlite3.connect('bookstore.db')
        cur = conn.cursor()

        # Запрос на извлечение данных о пользователях
        cur.execute("SELECT id, name, role, email, password FROM users")

        # Проходим по результатам запроса и добавляем их в listbox3
        for row in cur.fetchall():
            user_id, name, role, email, password = row
            user_info = f"{user_id}. {name} | Роль: {role} | Email: {email} | Пароль: {password}"
            listbox3.insert(tk.END, user_info)

        # Закрытие соединения
        conn.close()

        # Закрытие соединения с базой данных
        conn.close()



    # Вкладка "Главная"
    def setup_main_tab():
        label = tk.Label(tab_main,
                         text="Добро пожаловать в административную панель!\nВыберите вкладку для управления системой.",
                         font=("Arial", 14))
        label.pack(pady=20)

    # Вкладка "Продажи"
    def setup_sales_tab():
        global listbox
        listbox = tk.Listbox(tab_sales, width=100)
        listbox.pack(pady=10)

        entry_stock = tk.Entry(tab_sales)
        entry_stock.pack()
        tk.Button(tab_sales, text="Изменить остаток", command=lambda: update_stock(entry_stock, listbox)).pack(pady=5)
        tk.Button(tab_sales, text="Обновить список книг", command=show_books).pack()
        tk.Button(tab_sales, text="Добавить книгу", command=add_book).pack(pady=5)
        tk.Button(tab_sales, text="Редактировать выбранную книгу", command=edit_book).pack(pady=5)

        show_books()

    def show_books():
        if listbox:
            listbox.delete(0, tk.END)

        conn = sqlite3.connect('bookstore.db')
        cur = conn.cursor()

        # Обновленный запрос с учетом всех нужных полей
        cur.execute("""
            SELECT id, title, author, genre, publisher, year, isbn, sale_price, stock_quantity 
            FROM books
        """)

        for row in cur.fetchall():
            book_id, title, author, genre, publisher, year, isbn, sale_price, stock_quantity = row
            book_info = (
                f"ID:{book_id} | Название: {title} | Автор: {author} | Жанр: {genre} | "
                f"Издательство: {publisher} | Год: {year} | ISBN: {isbn} | "
                f"Цена: {sale_price:.2f} руб. | Остаток: {stock_quantity} шт."
            )
            listbox.insert(tk.END, book_info)

        conn.close()

    def update_stock(entry, listbox):
        selection = listbox.curselection()
        value = entry.get().strip()

        if not selection:
            messagebox.showwarning("Ошибка", "Выберите книгу")
            return
        if not value.isdigit():
            messagebox.showwarning("Ошибка", "Введите корректное целое число")
            return

        book_id = int(listbox.get(selection[0]).split('|')[0])
        new_stock = int(value)

        conn = sqlite3.connect('bookstore.db')
        cur = conn.cursor()
        cur.execute("UPDATE books SET stock_quantity = ? WHERE id = ?", (new_stock, book_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Успех", "Остаток обновлён")
        show_books()

    def add_book():
        def save():
            title = entry_title.get()
            author = entry_author.get()
            genre = entry_genre.get()
            publisher = entry_publisher.get()
            year = entry_year.get()
            isbn = entry_isbn.get()
            purchase_price = entry_purchase_price.get()
            sale_price = entry_sale_price.get()
            stock_quantity = entry_stock.get()
            description = entry_description.get("1.0", tk.END).strip()

            if not all([title, author, genre, publisher, year, isbn, purchase_price, sale_price, stock_quantity, description]):
                messagebox.showwarning("Ошибка", "Заполните все поля")
                return

            try:
                year = int(year)
                purchase_price = float(purchase_price)
                sale_price = float(sale_price)
                stock_quantity = int(stock_quantity)
            except ValueError:
                messagebox.showerror("Ошибка", "Проверьте формат числовых полей (год, цены, остаток)")
                return

            conn = sqlite3.connect('bookstore.db')
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO books (
                    title, author, genre, publisher, year,
                    isbn, purchase_price, sale_price, stock_quantity, description
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                title, author, genre, publisher, year,
                isbn, purchase_price, sale_price, stock_quantity, description
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Книга добавлена")
            add_win.destroy()
            show_books()

        add_win = tk.Toplevel(admin_root)
        add_win.title("Добавить книгу")



        def label_entry(parent, text):
            tk.Label(parent, text=text).pack()
            entry = tk.Entry(parent)
            entry.pack()
            return entry

        entry_title = label_entry(add_win, "Название книги")
        entry_author = label_entry(add_win, "Автор")
        entry_genre = label_entry(add_win, "Жанр")
        entry_publisher = label_entry(add_win, "Издательство")
        entry_year = label_entry(add_win, "Год издания")
        entry_isbn = label_entry(add_win, "ISBN")
        entry_purchase_price = label_entry(add_win, "Цена закупки")
        entry_sale_price = label_entry(add_win, "Цена продажи")
        entry_stock = label_entry(add_win, "Остаток")

        tk.Label(add_win, text="Описание").pack()
        entry_description = tk.Text(add_win, height=4, width=40)
        entry_description.pack()

        tk.Button(add_win, text="Сохранить", command=save).pack(pady=10)

    def edit_book():
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите книгу для редактирования")
            return

        book_data = listbox.get(selected[0]).split(" | ")
        book_id = int(
            book_data[0].split(":")[1])

        conn = sqlite3.connect('bookstore.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM books WHERE id=?", (book_id,))
        book = cur.fetchone()
        conn.close()

        if not book:
            messagebox.showerror("Ошибка", "Книга не найдена")
            return

        def save_changes():
            title = entry_title.get()
            author = entry_author.get()
            genre = entry_genre.get()
            publisher = entry_publisher.get()
            year = entry_year.get()
            isbn = entry_isbn.get()
            purchase_price = entry_purchase_price.get()
            sale_price = entry_sale_price.get()
            stock_quantity = entry_stock.get()
            description = entry_description.get("1.0", tk.END).strip()

            if not all([title, author, genre, publisher, year, isbn, purchase_price, sale_price, stock_quantity,
                        description]):
                messagebox.showwarning("Ошибка", "Заполните все поля")
                return

            try:
                year = int(year)
                purchase_price = float(purchase_price)
                sale_price = float(sale_price)
                stock_quantity = int(stock_quantity)
            except ValueError:
                messagebox.showerror("Ошибка", "Проверьте формат числовых полей (год, цены, остаток)")
                return

            conn = sqlite3.connect('bookstore.db')
            cur = conn.cursor()
            cur.execute("""
                UPDATE books SET
                    title=?, author=?, genre=?, publisher=?, year=?,
                    isbn=?, purchase_price=?, sale_price=?, stock_quantity=?, description=?
                WHERE id=?
            """, (
                title, author, genre, publisher, year,
                isbn, purchase_price, sale_price, stock_quantity, description,
                book_id
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Книга обновлена")
            edit_win.destroy()
            show_books()

        edit_win = tk.Toplevel()
        edit_win.title("Редактировать книгу")

        tk.Label(edit_win, text="Название книги").pack()
        entry_title = tk.Entry(edit_win)
        entry_title.insert(0, book[1])
        entry_title.pack()

        tk.Label(edit_win, text="Автор").pack()
        entry_author = tk.Entry(edit_win)
        entry_author.insert(0, book[2])
        entry_author.pack()

        tk.Label(edit_win, text="Жанр").pack()
        entry_genre = tk.Entry(edit_win)
        entry_genre.insert(0, book[3])
        entry_genre.pack()

        tk.Label(edit_win, text="Издательство").pack()
        entry_publisher = tk.Entry(edit_win)
        entry_publisher.insert(0, book[4])
        entry_publisher.pack()

        tk.Label(edit_win, text="Год издания").pack()
        entry_year = tk.Entry(edit_win)
        entry_year.insert(0, book[5])
        entry_year.pack()

        tk.Label(edit_win, text="ISBN").pack()
        entry_isbn = tk.Entry(edit_win)
        entry_isbn.insert(0, book[6])
        entry_isbn.pack()

        tk.Label(edit_win, text="Закупочная цена").pack()
        entry_purchase_price = tk.Entry(edit_win)
        entry_purchase_price.insert(0, book[7])
        entry_purchase_price.pack()

        tk.Label(edit_win, text="Цена продажи").pack()
        entry_sale_price = tk.Entry(edit_win)
        entry_sale_price.insert(0, book[8])
        entry_sale_price.pack()

        tk.Label(edit_win, text="Остаток").pack()
        entry_stock = tk.Entry(edit_win)
        entry_stock.insert(0, book[9])
        entry_stock.pack()

        tk.Label(edit_win, text="Описание").pack()
        entry_description = tk.Text(edit_win, height=4)
        entry_description.insert("1.0", book[10])
        entry_description.pack()

        tk.Button(edit_win, text="Сохранить изменения", command=save_changes).pack(pady=10)

    def setup_purchases_tab():
        def update_books_list():
            listbox2.delete(0, tk.END)
            cur.execute("SELECT id, title, stock_quantity FROM books")
            for row in cur.fetchall():
                listbox2.insert(tk.END, f"{row[0]} | {row[1]} | Остаток: {row[2]}")

        def add_supply():
            selection = listbox2.curselection()
            if not selection:
                messagebox.showwarning("Ошибка", "Выберите книгу из списка.")
                return

            book_line = listbox2.get(selection[0])
            book_id = int(book_line.split('|')[0])

            try:
                supplier_id = int(entry_supplier_id.get())
                quantity = int(entry_quantity.get())
                purchase_price = float(entry_price.get())
            except ValueError:
                messagebox.showwarning("Ошибка", "Введите корректные данные!")
                return

            # Добавление записи о поставке
            cur.execute(
                "INSERT INTO supplies (book_id, supplier_id, quantity, purchase_price, supply_date) VALUES (?, ?, ?, ?, DATE('now'))",
                (book_id, supplier_id, quantity, purchase_price))

            # Обновление остатков книги
            cur.execute("UPDATE books SET stock_quantity = stock_quantity + ? WHERE id = ?", (quantity, book_id))

            conn.commit()
            update_books_list()
            messagebox.showinfo("Успех", "Поставка добавлена и остаток обновлён.")

        # GUI
        label = tk.Label(tab_purchases, text="Управление поставками", font=("Arial", 14))
        label.pack(pady=10)

        listbox2 = tk.Listbox(tab_purchases, width=100)
        listbox2.pack(pady=10)

        # Ввод ID поставщика
        tk.Label(tab_purchases, text="ID поставщика:").pack()
        entry_supplier_id = tk.Entry(tab_purchases)
        entry_supplier_id.pack()

        # Ввод количества
        tk.Label(tab_purchases, text="Количество:").pack()
        entry_quantity = tk.Entry(tab_purchases)
        entry_quantity.pack()

        # Ввод закупочной цены
        tk.Label(tab_purchases, text="Закупочная цена:").pack()
        entry_price = tk.Entry(tab_purchases)
        entry_price.pack()

        # Кнопка добавить поставку
        tk.Button(tab_purchases, text="Добавить поставку", command=add_supply).pack(pady=10)

        # Обновить список книг
        tk.Button(tab_purchases, text="Обновить список книг", command=update_books_list).pack()

        update_books_list()

    def clear_user_fields():
        entry_name.delete(0, tk.END)
        entry_role.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_password.delete(0, tk.END)

    def show_users():
        listbox3.delete(0, tk.END)
        cur.execute("SELECT id, name, role, email FROM users")
        rows = cur.fetchall()
        for row in rows:
            display_text = f"{row[0]}. {row[1]} | {row[2]} | {row[3]}"
            listbox3.insert(tk.END, display_text)

    def add_user():
        name = entry_name.get().strip()
        role = entry_role.get().strip()
        email = entry_email.get().strip()
        password = entry_password.get().strip()

        if not name or not role or not email or not password:
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

        try:
            cur.execute(
                "INSERT INTO users (name, role, email, password) VALUES (?, ?, ?, ?)",
                (name, role, email, password)
            )
            conn.commit()
            clear_user_fields()
            show_users()
            messagebox.showinfo("Успех", "Пользователь добавлен")
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при добавлении пользователя:\n{e}")

    def edit_user():
        selected = listbox3.curselection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите пользователя для редактирования.")
            return

        index = selected[0]
        user_line = listbox3.get(index)
        user_id = int(user_line.split(".")[0])  # предполагается формат "1. Иван Иванов | role | email"

        name = entry_name.get().strip()
        role = entry_role.get().strip()
        email = entry_email.get().strip()
        password = entry_password.get().strip()

        if not name or not role or not email or not password:
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

        try:
            cur.execute(
                "UPDATE users SET name=?, role=?, email=?, password=? WHERE id=?",
                (name, role, email, password, user_id)
            )
            conn.commit()
            clear_user_fields()
            show_users()
            messagebox.showinfo("Успех", "Пользователь обновлён")
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при обновлении пользователя:\n{e}")

    def on_user_select(event):
        selected = listbox3.curselection()
        if not selected:
            return
        index = selected[0]

        # Загружаем всех пользователей (в том же порядке, что и в listbox)
        cur.execute("SELECT id, name, role, email, password FROM users")
        users = cur.fetchall()

        if index >= len(users):
            return

        user = users[index]  # (id, name, role, email, password)

        # Заполняем поля ввода
        entry_name.delete(0, tk.END)
        entry_name.insert(0, user[1])

        entry_role.delete(0, tk.END)
        entry_role.insert(0, user[2])

        entry_email.delete(0, tk.END)
        entry_email.insert(0, user[3])

        entry_password.delete(0, tk.END)
        entry_password.insert(0, user[4])

    #вкладке "Пользователи"
    def setup_stores_tab():
        # Создаем метку с текстом на вкладке "Пользователи"
        label = tk.Label(tab_stores, text="Управление пользователями", font=("Arial", 14))
        label.pack(pady=20)

        global listbox3
        global entry_user_data  # Поле для ввода данных пользователя

        global entry_name, entry_role, entry_email, entry_password
        global btn_add_user, btn_edit_user

        # Поля ввода данных пользователя
        frame_inputs = tk.Frame(tab_stores)
        frame_inputs.pack(pady=5)

        tk.Label(frame_inputs, text="Имя (ФИО)").grid(row=0, column=0, padx=5, pady=5)
        entry_name = tk.Entry(frame_inputs, width=25)
        entry_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_inputs, text="Роль").grid(row=0, column=2, padx=5, pady=5)
        entry_role = tk.Entry(frame_inputs, width=25)
        entry_role.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_inputs, text="Email").grid(row=1, column=0, padx=5, pady=5)
        entry_email = tk.Entry(frame_inputs, width=25)
        entry_email.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_inputs, text="Пароль").grid(row=1, column=2, padx=5, pady=5)
        entry_password = tk.Entry(frame_inputs, width=25)
        entry_password.grid(row=1, column=3, padx=5, pady=5)


        # Кнопки добавления и редактирования
        frame_buttons = tk.Frame(tab_stores)
        frame_buttons.pack(pady=10)

        btn_add_user = tk.Button(frame_buttons, text="Добавить клиента", command=add_user)
        btn_add_user.grid(row=0, column=0, padx=10)

        btn_edit_user = tk.Button(frame_buttons, text="Редактировать клиента", command=edit_user)
        btn_edit_user.grid(row=0, column=1, padx=10)


        # Создаем listbox для отображения пользователей
        listbox3 = tk.Listbox(tab_stores, width=100, height=20)
        listbox3.pack(pady=10)

        listbox3.bind('<<ListboxSelect>>', on_user_select)

        # Показываем список пользователей
        show_users()

    def setup_finances_tab():
        label = tk.Label(tab_finances, text="Финансовые отчеты", font=("Arial", 14))
        label.pack(pady=20)

        global listbox_finances

        # Создаем listbox для отображения заказов
        listbox_finances = tk.Listbox(tab_finances, width=100, height=20)
        listbox_finances.pack(pady=10)

        # Показываем список заказов
        show_orders()

    # Вкладка "Покупки"
    def show_orders():
        label = tk.Label(tab_crm, text="Список покупок", font=("Arial", 14))
        label.pack(pady=20)
        import sqlite3

        conn = sqlite3.connect('bookstore.db')
        cur = conn.cursor()

        cur.execute("SELECT id, user_id, book_id, quantity,price, order_date, status FROM orders")
        orders = cur.fetchall()

        listbox_finances.delete(0, tk.END)  # Очищаем список перед заполнением

        for order in orders:
            order_text = f"ID заказа: {order[0]} | ID пользователя: {order[1]} | ID книги: {order[2]} | Кол-во: {order[3]} | Цена: {order[4]} | Дата: {order[5]} | Статус: {order[6]}"
            listbox_finances.insert(tk.END, order_text)

        conn.close()

    # Вкладка "Корзина"
    def setup_crm_tab():
        label = tk.Label(tab_crm, text="Информация о корзине", font=("Arial", 14))
        label.pack(pady=20)

        global listbox_crm  # Делаем глобальным, чтобы потом обновлять

        listbox_crm = tk.Listbox(tab_crm, width=100, height=20)
        listbox_crm.pack(pady=10)

        show_cart_items()

    def show_cart_items():
        import sqlite3

        conn = sqlite3.connect('bookstore.db')
        cur = conn.cursor()

        try:
            cur.execute("""CREATE TABLE IF NOT EXISTS cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                book_id INTEGER,
                UNIQUE(user_id, book_id)
            )""")  # На всякий случай создаём таблицу, если вдруг нет

            cur.execute("SELECT id, user_id, book_id FROM cart")
            cart_items = cur.fetchall()

            listbox_crm.delete(0, tk.END)  # Очищаем список

            for item in cart_items:
                item_text = f"ID записи: {item[0]} | ID пользователя: {item[1]} | ID книги: {item[2]}"
                listbox_crm.insert(tk.END, item_text)
        except sqlite3.OperationalError as e:
            listbox_crm.insert(tk.END, "Ошибка загрузки данных: " + str(e))
        finally:
            conn.close()

    # Вкладка "Избранное"
    def setup_company_tab():
        label = tk.Label(tab_company, text="Избранное", font=("Arial", 14))
        label.pack(pady=20)

        global listbox_company  # Глобальная переменная для доступа к списку

        listbox_company = tk.Listbox(tab_company, width=100, height=20)
        listbox_company.pack(pady=10)

        show_favorites_items()

    def show_favorites_items():
        import sqlite3

        conn = sqlite3.connect('bookstore.db')
        cur = conn.cursor()

        try:
            # На всякий случай создаём таблицу, если вдруг нет
            cur.execute("""CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                book_id INTEGER,
                UNIQUE(user_id, book_id)
            )""")

            cur.execute("SELECT id, user_id, book_id FROM favorites")
            favorites_items = cur.fetchall()

            listbox_company.delete(0, tk.END)  # Очищаем список

            for item in favorites_items:
                item_text = f"ID записи: {item[0]} | ID пользователя: {item[1]} | ID книги: {item[2]}"
                listbox_company.insert(tk.END, item_text)

        except sqlite3.OperationalError as e:
            listbox_company.insert(tk.END, "Ошибка загрузки данных: " + str(e))
        finally:
            conn.close()

    # Вкладка "О компании"
    def setup_references_tab():
        label = tk.Label(tab_references, text="О компании", font=("Arial", 18, "bold"))
        label.pack(pady=10)

        info_text = (
            "Добро пожаловать в наш книжный магазин!\n\n"
            "Мы предлагаем широкий ассортимент книг различных жанров — от художественной литературы до научных изданий.\n"
            "Наша миссия — делать чтение доступным и вдохновляющим для каждого.\n\n"
            "Следите за нашими обновлениями и акциями!\n"
            "Спасибо, что выбираете нас."
        )

        text_widget = tk.Label(tab_references, text=info_text, font=("Arial", 12), justify="left", wraplength=600)
        text_widget.pack(padx=20, pady=10)

    def setup_reports_tab():
        label = tk.Label(tab_reports, text="Отчеты и аналитика", font=("Arial", 14))
        label.pack(pady=10)

        # Выбор периода для отчета по продажам
        frame_period = tk.Frame(tab_reports)
        frame_period.pack(pady=5)
        tk.Label(frame_period, text="С ").pack(side=tk.LEFT)
        entry_start = tk.Entry(frame_period)
        entry_start.insert(0, "2024-01-01")
        entry_start.pack(side=tk.LEFT)
        tk.Label(frame_period, text=" по ").pack(side=tk.LEFT)
        entry_end = tk.Entry(frame_period)
        entry_end.insert(0, datetime.now().strftime("%Y-%m-%d"))
        entry_end.pack(side=tk.LEFT)

        tk.Button(tab_reports, text="Отчет по продажам за период",
                  command=lambda: report_sales(entry_start.get(), entry_end.get())).pack(pady=5)
        tk.Button(tab_reports, text="Остатки на складе", command=report_stock).pack(pady=5)
        tk.Button(tab_reports, text="Популярные товары", command=report_popular_books).pack(pady=5)
        tk.Button(tab_reports, text="Прибыль и расходы", command=report_profit_and_expense).pack(pady=5)

        global text_report
        text_report = tk.Text(tab_reports, height=20, width=100)
        text_report.pack(pady=10)
        text_widget = tk.Message(tab_reports, text="", font=("Arial", 12), width=600, justify="left")
        text_widget.pack(padx=20, pady=10)

    def report_sales(start_date, end_date):
        import sqlite3

        conn = sqlite3.connect("bookstore.db")
        cur = conn.cursor()

        cur.execute("""
            SELECT b.title, SUM(o.quantity) AS qty, SUM(o.quantity * o.price) AS total
            FROM orders o
            JOIN books b ON o.book_id = b.id
            WHERE o.order_date BETWEEN ? AND ?
            GROUP BY o.book_id
        """, (start_date, end_date))

        rows = cur.fetchall()
        conn.close()

        text_report.delete(1.0, tk.END)
        text_report.insert(tk.END, f"Отчет по продажам с {start_date} по {end_date}:\n")

        if rows:
            for row in rows:
                text_report.insert(tk.END, f"Книга: {row[0]} | Продано: {row[1]} шт. | Сумма: {row[2]:.2f} руб.\n")
        else:
            text_report.insert(tk.END, "За указанный период продаж не найдено.")

    def report_stock():
        conn = sqlite3.connect("bookstore.db")
        cur = conn.cursor()
        cur.execute("SELECT title, stock_quantity FROM books")
        rows = cur.fetchall()
        conn.close()

        text_report.delete(1.0, tk.END)
        text_report.insert(tk.END, "Остатки на складе:\n")
        for row in rows:
            text_report.insert(tk.END, f"{row[0]}: {row[1]} шт.\n")

    def report_popular_books():
        conn = sqlite3.connect("bookstore.db")
        cur = conn.cursor()
        cur.execute("""
            SELECT b.title, SUM(s.quantity) AS total_sold
            FROM orders s
            JOIN books b ON s.book_id = b.id
            GROUP BY s.book_id
            ORDER BY total_sold DESC
            LIMIT 5
        """)
        rows = cur.fetchall()
        conn.close()

        text_report.delete(1.0, tk.END)
        text_report.insert(tk.END, "Популярные товары (ТОП 5):\n")
        for row in rows:
            text_report.insert(tk.END, f"{row[0]} — продано: {row[1]} шт.\n")

    def report_profit_and_expense():
        import sqlite3

        conn = sqlite3.connect("bookstore.db")
        cur = conn.cursor()

        # Общий доход — сумма количества * цены из заказов
        cur.execute("SELECT SUM(quantity * price) FROM orders")
        revenue = cur.fetchone()[0] or 0.0

        # Общие расходы — сумма закупочной цены * количества из закупок
        cur.execute("SELECT SUM(purchase_price * quantity) FROM purchases")
        expenses = cur.fetchone()[0] or 0.0

        profit = revenue - expenses

        conn.close()

        text_report.delete(1.0, tk.END)
        text_report.insert(tk.END, "Финансовый отчет:\n")
        text_report.insert(tk.END, f"Доход от продаж: {revenue:.2f} руб.\n")
        text_report.insert(tk.END, f"Расходы на закупку: {expenses:.2f} руб.\n")
        text_report.insert(tk.END, f"Прибыль: {profit:.2f} руб.\n")

    # Инициализация вкладок
    def setup_tabs():
        setup_main_tab()
        setup_sales_tab()
        setup_purchases_tab()
        setup_stores_tab()
        setup_finances_tab()
        setup_crm_tab()
        setup_company_tab()
        setup_references_tab()
        setup_reports_tab()

    # Функция для обновления содержимого вкладки
    def update_content(event, tab_control):
        current_tab = tab_control.select()
        if current_tab == tab_sales:
            setup_sales_tab()
        elif current_tab == tab_main:
            setup_main_tab()
        elif current_tab == tab_purchases:
            setup_purchases_tab()
        elif current_tab == tab_stores:
            setup_stores_tab()
        elif current_tab == tab_finances:
            setup_finances_tab()
        elif current_tab == tab_crm:
            setup_crm_tab()
        elif current_tab == tab_company:
            setup_company_tab()
        elif current_tab == tab_references:
            setup_references_tab()
        elif current_tab == tab_reports:
            setup_reports_tab()



    # Привязка события смены вкладки
    tab_control.bind("<<NotebookTabChanged>>", lambda event: update_content(event, tab_control))

    # Инициализация содержимого первой вкладки
    setup_tabs()

    admin_root.mainloop()

# Запуск
if __name__ == "__main__":
    admin_login()






