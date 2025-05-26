import tkinter as tk
from tkinter import messagebox
import sqlite3


# Глобальные переменные
current_user = None
cart = []
conn = None
cur = None

def open_db():
    global conn, cur
    conn = sqlite3.connect('bookstore.db', timeout=10)  # Увеличен timeout
    cur = conn.cursor()
    conn.execute('PRAGMA journal_mode=WAL')  # Включаем режим WAL для улучшения работы с несколькими соединениями

def close_db():
    global conn, cur
    if conn:
        conn.commit()
        cur.close()
        conn.close()

# ----------------------------- Вход и регистрация -----------------------------
def user_login_register():
    def register():
        name = entry_name.get().strip()
        email = entry_email.get().strip()
        password = entry_password.get().strip()  # Получаем пароль из нового поля

        if name and email and password:
            try:
                open_db()
                # Создаем таблицу, если она еще не существует
                cur.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY, 
                    name TEXT, 
                    email TEXT UNIQUE, 
                    password TEXT NOT NULL
                )""")

                # Проверка на существующий email
                cur.execute("SELECT id FROM users WHERE email = ?", (email,))
                user = cur.fetchone()
                if user:
                    # Если пользователь с таким email существует, логиним его
                    global current_user
                    current_user = user[0]
                    messagebox.showinfo("Добро пожаловать", "Вы вошли как существующий пользователь.")
                    login_win.destroy()
                    open_user_interface()
                else:
                    # Если пользователя с таким email нет, регистрируем нового
                    cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
                    conn.commit()
                    # Получаем id только что зарегистрированного пользователя
                    current_user = cur.lastrowid
                    messagebox.showinfo("Успешно", "Вы зарегистрированы и вошли в систему.")
                    login_win.destroy()
                    open_user_interface()

            except sqlite3.Error as e:
                messagebox.showerror("Ошибка", f"Ошибка базы данных:\n{e}")
                print(f"Ошибка базы данных: {e}")
            finally:
                close_db()
        else:
            messagebox.showwarning("Недостаточно данных", "Пожалуйста, введите имя, email и пароль.")

    login_win = tk.Tk()
    login_win.title("Вход / Регистрация")
    login_win.configure(bg="grey")
    tk.Label(login_win, text="Имя:").pack()
    entry_name = tk.Entry(login_win)
    entry_name.pack()

    tk.Label(login_win, text="Email:").pack()
    entry_email = tk.Entry(login_win)
    entry_email.pack()

    tk.Label(login_win, text="Пароль:").pack()  # Добавляем поле для пароля
    entry_password = tk.Entry(login_win, show="*")  # Скрываем ввод пароля
    entry_password.pack()

    tk.Button(login_win, text="Войти / Зарегистрироваться", command=register).pack()
    def back_to_main_menu():
        import main  # импорт внутри функции
        login_win.destroy()
        main.main_menu()
    button_frame = tk.Frame(login_win)  # Создаем контейнер для кнопок
    button_frame.pack(fill=tk.X)  # Контейнер растягивается на всю ширину окна
    button_frame.configure(bg="grey")
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


# ----------------------------- Основной интерфейс -----------------------------
def open_user_interface():
    root = tk.Tk()
    root.title("Книжный магазин")

    def load_books(search_query=None):
        listbox.delete(0, tk.END)
        try:
            open_db()
            cur.execute("""CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                genre TEXT,
                publisher TEXT,
                year INTEGER,
                isbn TEXT,
                purchase_price REAL,
                sale_price REAL,
                stock_quantity INTEGER,
                description TEXT
            )""")

            if search_query:
                cur.execute("""
                    SELECT id, title, author, sale_price FROM books 
                    WHERE stock_quantity > 0 AND title LIKE ?
                    """, ('%' + search_query + '%',))
            else:
                cur.execute("""
                    SELECT id, title, author, sale_price FROM books 
                    WHERE stock_quantity > 0
                    """)

            for row in cur.fetchall():
                listbox.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]} | Цена: {row[3]} руб.")

        except sqlite3.OperationalError as e:
            messagebox.showerror("Ошибка", f"Ошибка базы данных:\n{e}")
            print(f"Ошибка базы данных: {e}")

        finally:
            close_db()

    # Добавление книги в корзину
    def add_to_cart():
        selection = listbox.curselection()
        if selection:
            book_id = int(listbox.get(selection[0]).split('|')[0])
            try:
                open_db()
                cur.execute("""CREATE TABLE IF NOT EXISTS cart (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    book_id INTEGER,
                    UNIQUE(user_id, book_id)
                )""")
                cur.execute("INSERT OR IGNORE INTO cart (user_id, book_id) VALUES (?, ?)",
                            (current_user, book_id))
                conn.commit()
                messagebox.showinfo("Корзина", "Книга добавлена в корзину.")
            except sqlite3.OperationalError as e:
                messagebox.showerror("Ошибка", f"Ошибка базы данных:\n{e}")
                print(f"Ошибка базы данных: {e}")
            finally:
                close_db()

    # Добавление в избранное
    def add_to_favorites():
        selection = listbox.curselection()
        if selection:
            book_id = int(listbox.get(selection[0]).split('|')[0])
            try:
                open_db()
                cur.execute("""CREATE TABLE IF NOT EXISTS favorites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    book_id INTEGER,
                    UNIQUE(user_id, book_id)
                )""")
                cur.execute("INSERT OR IGNORE INTO favorites (user_id, book_id) VALUES (?, ?)",
                            (current_user, book_id))
                conn.commit()
                messagebox.showinfo("Избранное", "Книга добавлена в избранное.")
            except sqlite3.OperationalError as e:
                messagebox.showerror("Ошибка", f"Ошибка базы данных:\n{e}")
                print(f"Ошибка базы данных: {e}")
            finally:
                close_db()

    def show_bonus_card():
        # Создаем новое окно для бонусной карты
        bonus_window = tk.Toplevel()
        bonus_window.title("Бонусная карта")

        # Заглушка Состоящие из текстовых меток
        tk.Label(bonus_window, text="Бонусная карта 89373570339", font=("Arial", 14)).pack(pady=5)
        tk.Label(bonus_window, text="Тип карты: Бонусная").pack(pady=5)
        tk.Label(bonus_window, text="Телефон: 89136429513").pack(pady=5)
        tk.Label(bonus_window, text="Имя владельца: Илова Арина").pack(pady=5)
        tk.Label(bonus_window, text="Email для связи: example@example.com").pack(pady=5)
        tk.Label(bonus_window, text="Контрагент: Баранова Анна Александровна").pack(pady=5)

        # Заглушка Баллы и продажи
        tk.Label(bonus_window, text="Информация о баллах на карте и продажах", font=("Arial", 12)).pack(pady=5)
        tk.Label(bonus_window, text="Начислено баллов: 300").pack(pady=5)
        tk.Label(bonus_window, text="Потрачено баллов: 60").pack(pady=5)
        tk.Label(bonus_window, text="Общая сумма продаж: 600.00 руб.").pack(pady=5)
        tk.Label(bonus_window, text="Последняя продажа: 24.04.2025").pack(pady=5)

        # Заглушка История начислений
        tk.Label(bonus_window, text="История начисления и списания баллов на карте", font=("Arial", 12)).pack(pady=5)
        tk.Label(bonus_window, text="1. 24.04.2025 Начислено 80.00 руб.").pack(pady=5)
        tk.Label(bonus_window, text="2. 24.04.2025 Начислено 160.00 руб.").pack(pady=5)
        tk.Label(bonus_window, text="3. 24.04.2025 Чек No170911153218300027 от 11.09. Потрачено 60.00 руб.").pack(
            pady=5)
        tk.Label(bonus_window, text="4. 24.04.2025 Чек No170911153818300028 от 11.09. Потрачено 30.00 руб.").pack(
            pady=5)
        tk.Label(bonus_window, text="5. 24.04.2025 Чек No170911154318300029 от 11.09. Потрачено 30.00 руб.").pack(
            pady=5)

        # Кнопка для оформления покупки
        def on_confirm_purchase():
            messagebox.showinfo("Успешно", "Заказ оформлен.")
            bonus_window.destroy()  # Закрытие окна бонусной карты после оформления

        tk.Button(bonus_window, text="Оформить покупку", command=on_confirm_purchase).pack(pady=10)

        # Кнопка для закрытия окна
        tk.Button(bonus_window, text="Закрыть", command=bonus_window.destroy).pack(pady=10)

    def place_order():
        try:
            open_db()

            # Проверяем, есть ли книги в корзине текущего пользователя
            cur.execute("SELECT book_id FROM cart WHERE user_id = ?", (current_user,))
            cart_books = cur.fetchall()

            if not cart_books:
                messagebox.showwarning("Корзина пуста", "Сначала добавьте книги в корзину.")
                return


            # Оформляем заказ
            for book in cart_books:
                book_id = book[0]

                # Получаем цену книги на момент заказа
                cur.execute("SELECT sale_price FROM books WHERE id = ?", (book_id,))
                price_result = cur.fetchone()
                if price_result:
                    price = price_result[0]
                else:
                    price = 0.0  # или можно выдать ошибку

                cur.execute(
                    "INSERT INTO orders (user_id, book_id, quantity, price, status) VALUES (?, ?, ?, ?, ?)",
                    (current_user, book_id, 1, price, 'Ожидает обработки')
                )

                # Обновляем количество книг на складе
                cur.execute("UPDATE books SET stock_quantity = stock_quantity - 1 WHERE id = ?", (book_id,))

            # Удаляем книги из корзины после оформления заказа
            cur.execute("DELETE FROM cart WHERE user_id = ?", (current_user,))

            conn.commit()

            show_bonus_card()
            # Обновляем интерфейс
            cart.clear()
            load_books()

        except sqlite3.OperationalError as e:
            messagebox.showerror("Ошибка", f"Ошибка базы данных:\n{e}")
            print(f"Ошибка базы данных: {e}")
        finally:
            close_db()

    def show_details():
        selection = listbox.curselection()
        if not selection:
            return
        # Получаем id книги из выбранной строки (разделяем по '|' и берем первый элемент)
        book_id = int(listbox.get(selection[0]).split('|')[0])
        try:
            open_db()  # Предполагается, что эта функция открывает соединение и инициализирует cur
            cur.execute("""
                SELECT title, author, description, sale_price, genre, publisher, year, isbn, stock_quantity 
                FROM books 
                WHERE id = ?
            """, (book_id,))
            book = cur.fetchone()
            if book:
                detail_win = tk.Toplevel(root)
                detail_win.title("Информация о книге")

                tk.Label(detail_win, text=f"Название: {book[0]}").pack()
                tk.Label(detail_win, text=f"Автор: {book[1]}").pack()
                tk.Label(detail_win, text=f"Жанр: {book[4]}").pack()
                tk.Label(detail_win, text=f"Издательство: {book[5]}").pack()
                tk.Label(detail_win, text=f"Год издания: {book[6]}").pack()
                tk.Label(detail_win, text=f"ISBN: {book[7]}").pack()
                tk.Label(detail_win, text=f"Описание: {book[2]}").pack()
                tk.Label(detail_win, text=f"Цена продажи: {book[3]} руб.").pack()
                tk.Label(detail_win, text=f"Количество на складе: {book[8]}").pack()
        except sqlite3.OperationalError as e:
            messagebox.showerror("Ошибка", f"Ошибка базы данных:\n{e}")
            print(f"Ошибка базы данных: {e}")
        finally:
            close_db()  # Предполагается, что эта функция закрывает соединение

    # История заказов
    def show_order_history():
        try:
            open_db()
            cur.execute("SELECT b.title, o.quantity, o.status FROM orders o JOIN books b ON o.book_id = b.id WHERE o.user_id = ?", (current_user,))
            orders = cur.fetchall()
            order_win = tk.Toplevel(root)
            order_win.title("История заказов")
            for order in orders:
                tk.Label(order_win, text=f"{order[0]} — {order[1]} шт. — Статус: {order[2]}").pack()
        except sqlite3.OperationalError as e:
            messagebox.showerror("Ошибка", f"Ошибка базы данных:\n{e}")
            print(f"Ошибка базы данных: {e}")
        finally:
            close_db()

    # Избранное
    def show_favorites():
        try:
            open_db()
            cur.execute(
                "SELECT b.id, b.title, b.author FROM favorites f JOIN books b ON f.book_id = b.id WHERE f.user_id = ?",
                (current_user,))
            favorites_list = cur.fetchall()
            fav_win = tk.Toplevel(root)
            fav_win.title("Избранные книги")

            fav_listbox = tk.Listbox(fav_win, width=60)
            fav_listbox.pack()

            # Заполняем Listbox избранными книгами
            for book in favorites_list:
                fav_listbox.insert(tk.END, f"{book[0]} | {book[1]} | {book[2]}")

            # Функция для удаления книги из избранного
            def remove_from_favorites():
                selection = fav_listbox.curselection()
                if selection:
                    book_id = int(fav_listbox.get(selection[0]).split('|')[0])  # Получаем book_id
                    try:
                        open_db()
                        # Удаляем книгу из таблицы избранного
                        cur.execute("DELETE FROM favorites WHERE user_id = ? AND book_id = ?", (current_user, book_id))
                        conn.commit()

                        # Обновляем интерфейс, удаляя книгу из списка
                        fav_listbox.delete(selection[0])
                        messagebox.showinfo("Избранное", "Книга удалена из избранного.")
                    except sqlite3.OperationalError as e:
                        messagebox.showerror("Ошибка", f"Ошибка базы данных:\n{e}")
                        print(f"Ошибка базы данных: {e}")
                    finally:
                        close_db()

            # Кнопка для удаления книги из избранного
            remove_button = tk.Button(fav_win, text="Удалить из избранного", command=remove_from_favorites)
            remove_button.pack()

        except sqlite3.OperationalError as e:
            messagebox.showerror("Ошибка", f"Ошибка базы данных:\n{e}")
            print(f"Ошибка базы данных: {e}")
        finally:
            close_db()

    # Корзина
    def show_cart():
        cart_win = tk.Toplevel(root)
        cart_win.title("Корзина")
        cart_listbox = tk.Listbox(cart_win, width=60)
        cart_listbox.pack()

        def remove_from_cart():
            selection = cart_listbox.curselection()
            if selection:
                # Получаем выбранный элемент
                selected_item = cart_listbox.get(selection[0])
                book_id = int(selected_item.split('|')[0].strip())  # Извлекаем book_id

                try:
                    open_db()
                    # Удаляем книгу из корзины
                    cur.execute("DELETE FROM cart WHERE user_id = ? AND book_id = ?", (current_user, book_id))
                    conn.commit()
                    # Удаляем книгу из списка отображаемых элементов
                    cart_listbox.delete(selection[0])
                    messagebox.showinfo("Удалено", "Книга удалена из корзины.")
                except sqlite3.OperationalError as e:
                    messagebox.showerror("Ошибка", f"Ошибка базы данных:\n{e}")
                    print(f"Ошибка базы данных: {e}")
                finally:
                    close_db()

        try:
            open_db()
            cart_items = []
            # Извлекаем книги, которые добавлены в корзину для текущего пользователя
            cur.execute("SELECT book_id FROM cart WHERE user_id = ?", (current_user,))
            cart_books = cur.fetchall()

            # Для каждой книги в корзине получаем её название
            for book in cart_books:
                book_id = book[0]
                cur.execute("SELECT title FROM books WHERE id = ?", (book_id,))
                book = cur.fetchone()
                if book:
                    cart_items.append((book_id, book[0]))

            # Отображаем книги в списке
            for item in cart_items:
                cart_listbox.insert(tk.END, f"{item[0]} | {item[1]}")

            # Кнопка для удаления книги из корзины
            remove_button = tk.Button(cart_win, text="Удалить из корзины", command=remove_from_cart)
            remove_button.pack(pady=10)

        except sqlite3.OperationalError as e:
            messagebox.showerror("Ошибка", f"Ошибка базы данных:\n{e}")
            print(f"Ошибка базы данных: {e}")
        finally:
            close_db()

    def back_to_main_menu():
        import main  # импорт внутри функции
        root.destroy()
        main.main_menu()

    # Элементы интерфейса
    button_frame = tk.Frame(root)  # Создаем контейнер для кнопок
    button_frame.pack(fill=tk.X)  # Контейнер растягивается на всю ширину окна
    button_frame.configure(bg="grey")

    # Кнопки в одну строку
    tk.Button(button_frame, text="Обновить каталог", command=load_books).pack(side=tk.LEFT)
    tk.Button(button_frame, text="Инфо о книге", command=show_details).pack(side=tk.LEFT)
    tk.Button(button_frame, text="Добавить в корзину", command=add_to_cart).pack(side=tk.LEFT)
    tk.Button(button_frame, text="Добавить в избранное", command=add_to_favorites).pack(side=tk.LEFT)
    tk.Button(button_frame, text="Оформить заказ", command=place_order).pack(side=tk.LEFT)
    tk.Button(button_frame, text="История заказов", command=show_order_history).pack(side=tk.LEFT)
    tk.Button(button_frame, text="Избранное", command=show_favorites).pack(side=tk.LEFT)
    tk.Button(button_frame, text="Корзина", command=show_cart).pack(side=tk.LEFT)




    exit_button = tk.Button(
        button_frame,
        text="Выход",
        command=root.destroy,
        bg="red",
        fg="white",
        activebackground="darkred",
        activeforeground="white",
        font=("Arial", 10, "bold")
    )
    exit_button.pack(side=tk.LEFT)

    tk.Label(root, text="Поиск книг:").pack()
    entry_search = tk.Entry(root, width=120)
    entry_search.pack()
    tk.Button(root, text="Найти", command=lambda: load_books(entry_search.get())).pack()

    listbox = tk.Listbox(root, width=120)
    listbox.pack()



    load_books()

    button_bot_frame = tk.Frame(root)  # Создаем контейнер для кнопок
    button_bot_frame.pack(fill=tk.X, pady=10)  # Контейнер растягивается на всю ширину окна
    button_bot_frame.configure(bg="grey")
    back_to_menu_button = tk.Button(
        button_bot_frame,
        text="В главное меню",
        command=back_to_main_menu,
        bg="blue",
        fg="white",
        activebackground="darkblue",
        activeforeground="white",
        font=("Arial", 10, "bold")
    )

    # Размещение кнопки по центру контейнера
    back_to_menu_button.pack(side=tk.TOP, pady=10)  # Кнопка выравнивается по центру

    root.mainloop()

# ----------------------------- Запуск -----------------------------
if __name__ == '__main__':
    user_login_register()
