import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox


def admin_login():
    def login():
        if entry_code.get() == "admin123":
            login_win.destroy()
            open_admin_panel()
        else:
            messagebox.showerror("Ошибка", "Неверный код администратора")

    login_win = tk.Tk()
    login_win.title("Вход администратора")

    tk.Label(login_win, text="Введите код администратора:").pack(pady=5)
    entry_code = tk.Entry(login_win, show="*")
    entry_code.pack(pady=5)
    tk.Button(login_win, text="Войти", command=login).pack(pady=5)
    login_win.mainloop()


def open_admin_panel():

    admin_root = tk.Tk()
    admin_root.title("Панель администратора")

    conn = sqlite3.connect('bookstore.db')
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        book_id INTEGER,
        quantity INTEGER,
        order_date TEXT DEFAULT (datetime('now')),
        status TEXT DEFAULT 'в обработке',
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(book_id) REFERENCES books(id)
    );
    """)

    conn.commit()

    # === Создаем общий фрейм для вкладок и кнопки выхода ===
    top_frame = tk.Frame(admin_root)
    top_frame.pack(fill="x")  # растянуть по ширине

    # === Создаем вкладки ===
    tab_control = ttk.Notebook(top_frame)


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



    tab_control.pack(side=tk.LEFT, fill="x", expand=True)  # вкладки влево, растягиваются

    def back_to_main_menu():
        import main  # импорт внутри функции
        admin_root.destroy()
        main.main_menu()

        # Элементы интерфейса

    button_frame = tk.Frame(admin_root)  # Создаем контейнер для кнопок
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


    def show_orders():
        # Очищаем список перед загрузкой новых данных
        if listbox2:
            listbox2.delete(0, tk.END)

        # Подключаемся к базе данных
        conn = sqlite3.connect('bookstore.db')
        cur = conn.cursor()

        # Запрос на извлечение данных о заказах
        cur.execute("""
            SELECT orders.id, users.username, books.title, orders.quantity, orders.order_date, orders.status
            FROM orders
            JOIN users ON orders.user_id = users.id
            JOIN books ON orders.book_id = books.id
        """)

        # Проходим по результатам запроса и добавляем их в listbox
        for row in cur.fetchall():
            # Формируем строку для отображения
            order_info = f"Заказ ID: {row[0]} | Пользователь: {row[1]} | Книга: {row[2]} | Количество: {row[3]} | Дата заказа: {row[4]} | Статус: {row[5]}"
            # Добавляем строку в listbox
            if listbox2:
                listbox2.insert(tk.END, order_info)

        # Закрываем соединение с базой данных
        conn.close()

    # Функция для отображения пользователей в listbox
    def show_users():
        # Очистка listbox перед добавлением новых данных
        if listbox3:
            listbox3.delete(0, tk.END)

        # Подключаемся к базе данных
        conn = sqlite3.connect('bookstore.db')
        cur = conn.cursor()

        # Запрос на извлечение данных о пользователях
        cur.execute("SELECT name, email, password FROM users")

        # Проходим по результатам запроса и добавляем их в listbox3
        for row in cur.fetchall():
            user_info = f"Имя пользователя: {row[0]} | Email: {row[1]} | Пароль: {row[2]}"
            if listbox3:
                listbox3.insert(tk.END, user_info)

        # Закрытие соединения с базой данных
        conn.close()

    def show_books():
        if listbox:
            listbox.delete(0, tk.END)
        conn = sqlite3.connect('bookstore.db')
        cur = conn.cursor()
        cur.execute("SELECT id, title, author, price, stock FROM books")
        for row in cur.fetchall():
            if listbox:
                listbox.insert(tk.END, f"{row[0]} | {row[1]} | Автор: {row[2]} | Цена: {row[3]} | В наличии: {row[4]}")
        conn.close()

    def update_stock():
        global entry_stock
        entry_stock = tk.Entry(admin_root)

        selection = listbox.curselection()
        if not selection or not entry_stock.get().isdigit():
            messagebox.showwarning("Ошибка", "Выберите книгу и введите количество")
            return
        book_id = int(listbox.get(selection[0]).split('|')[0])
        new_stock = int(entry_stock.get())
        conn = sqlite3.connect('bookstore.db')
        cur = conn.cursor()
        cur.execute("UPDATE books SET stock = ? WHERE id = ?", (new_stock, book_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Успех", "Остаток обновлён")
        show_books()

    def add_book():
        def save():
            try:
                conn = sqlite3.connect('bookstore.db')
                cur = conn.cursor()
                cur.execute("INSERT INTO books (title, author, description, price, stock) VALUES (?, ?, ?, ?, ?)",
                            (title.get(), author.get(), desc.get(), float(price.get()), int(stock.get())))
                conn.commit()
                conn.close()
                messagebox.showinfo("Успех", "Книга добавлена")
                add_win.destroy()
                show_books()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка добавления: {e}")

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

        tk.Button(add_win, text="Сохранить", command=save).pack(pady=10)

    # Вкладка "Главная"
    def setup_main_tab():
        label = tk.Label(tab_main,
                         text="Добро пожаловать в административную панель!\nВыберите вкладку для управления системой.",
                         font=("Arial", 14))
        label.pack(pady=20)

    # Вкладка "Продажи"
    def setup_sales_tab():
        global listbox
        global entry_stock
        listbox = tk.Listbox(tab_sales, width=100)
        listbox.pack(pady=10)

        entry_stock = tk.Entry(tab_sales)
        entry_stock.pack()
        tk.Button(tab_sales, text="Изменить остаток", command=update_stock).pack(pady=5)
        tk.Button(tab_sales, text="Обновить список книг", command=show_books).pack()
        tk.Button(tab_sales, text="Добавить книгу", command=add_book).pack(pady=5)

        show_books()


    # Вкладка "Закупки"
    def setup_purchases_tab():
        label = tk.Label(tab_purchases, text="Управление закупками", font=("Arial", 14))
        label.pack(pady=20)
        global listbox2
        global entry_stock
        listbox2 = tk.Listbox(tab_purchases, width=100)
        listbox2.pack(pady=10)

        entry_stock = tk.Entry(tab_purchases)
        entry_stock.pack()
        tk.Button(tab_purchases, text="Изменить остаток", command=update_stock).pack(pady=5)
        tk.Button(tab_purchases, text="Обновить список книг", command=show_books).pack()
        tk.Button(tab_purchases, text="Добавить книгу", command=add_book).pack(pady=5)

        show_books()
    #вкладке "Пользователи"
    def setup_stores_tab():
        # Создаем метку с текстом на вкладке "Пользователи"
        label = tk.Label(tab_stores, text="Управление пользователями", font=("Arial", 14))
        label.pack(pady=20)

        global listbox3
        global entry_user_data  # Поле для ввода данных пользователя

        # Создаем listbox для отображения пользователей
        listbox3 = tk.Listbox(tab_stores, width=100, height=20)
        listbox3.pack(pady=10)


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

        cur.execute("SELECT id, user_id, book_id, quantity, order_date, status FROM orders")
        orders = cur.fetchall()

        listbox_finances.delete(0, tk.END)  # Очищаем список перед заполнением

        for order in orders:
            order_text = f"ID заказа: {order[0]} | ID пользователя: {order[1]} | ID книги: {order[2]} | Кол-во: {order[3]} | Дата: {order[4]} | Статус: {order[5]}"
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


    # Привязка события смены вкладки
    tab_control.bind("<<NotebookTabChanged>>", lambda event: update_content(event, tab_control))

    # Инициализация содержимого первой вкладки
    setup_tabs()

    admin_root.mainloop()

# Запуск
if __name__ == "__main__":
    admin_login()






