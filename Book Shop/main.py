# Стандартные библиотеки
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3

# Сторонние библиотеки
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Настройки ключа для шифрования
SECRET_KEY = b"shortkey".ljust(16, b'0')

def encrypt_password(password):
    """ Функция для шифрования паролей """
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(password.encode(), AES.block_size))
    return base64.b64encode(cipher.iv + ct_bytes).decode()


def decrypt_password(enc_password):
    """ Функция для дешифрования паролей """
    data = base64.b64decode(enc_password)
    iv = data[:AES.block_size]
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(data[AES.block_size:]), AES.block_size).decode()


def init_db():
    """ Заглушка, если вдруг понадобится расширение в будущем """
    pass

class BookstoreApp:
    """ Основной класс для функционирования программы """

    def __init__(self, root):
        """ Инициализация графического интерфейса  """
        self.root = root
        self.root.title("Книжный магазин")
        self.root.geometry("980x480")
        self.root.resizable(False, False)
        self.conn = sqlite3.connect("bookstore.db")
        self.cursor = self.conn.cursor()
        self.user = None
        self.show_auth_menu()

    def show_auth_menu(self):
        """ Функция меню выбора авторизации или регистрации """
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root)
        frame.pack(expand=True)

        tk.Label(frame, text="Книжный магазин", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Button(frame, text="Вход", width=15, command=self.show_login).pack(pady=10)
        tk.Button(frame, text="Регистрация", width=15, command=self.show_register).pack(pady=10)

    def show_login(self):
        """ Функция авторизации """
        self.clear_window()
        frame = tk.Frame(self.root)
        frame.pack(expand=True)

        tk.Label(frame, text="Авторизация", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(frame, text="Логин").pack()
        self.login_entry = tk.Entry(frame)
        self.login_entry.pack()

        tk.Label(frame, text="Пароль").pack()
        self.password_entry = tk.Entry(frame, show="*")
        self.password_entry.pack()

        tk.Button(frame, text="Войти", command=self.login).pack(pady=10)

    def show_register(self):
        """ Функция регистрации """
        self.clear_window()
        frame = tk.Frame(self.root)
        frame.pack(expand=True)

        tk.Label(frame, text="Регистрация", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(frame, text="Новый логин").pack()
        self.reg_login_entry = tk.Entry(frame)
        self.reg_login_entry.pack()

        tk.Label(frame, text="Пароль").pack()
        self.reg_password_entry = tk.Entry(frame, show="*")
        self.reg_password_entry.pack()

        tk.Button(frame, text="Зарегистрироваться", command=self.register).pack(pady=10)

    def login(self):
        """ Функция проверки введеных данных для входа """
        username = self.login_entry.get()
        password = self.password_entry.get()

        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = self.cursor.fetchone()

        if user and decrypt_password(user[2]) == password:
            self.user = user
            self.show_main_interface()
        else:
            messagebox.showerror("Ошибка", "Неверные данные")

    def register(self):
        """ Фунция регистрации нового пользователя """
        username = self.reg_login_entry.get()
        password = self.reg_password_entry.get()

        try:
            self.cursor.execute("INSERT INTO users (username, password, role, balance) VALUES (?, ?, ?, ?)",
                                (username, encrypt_password(password), "buyer", 1000))
            self.conn.commit()
            messagebox.showinfo("Успех", "Регистрация прошла успешно!")
            self.show_auth_menu()
        except sqlite3.IntegrityError:
            messagebox.showerror("Ошибка", "Пользователь уже существует")

    def clear_window(self):
        """ Функция для очистки интерфейса для перехода на другую страницу"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_interface(self):
        """ Функция основного меню программы"""
        self.clear_window()

        frame = tk.Frame(self.root)
        frame.pack()

        if self.user[3] == "buyer":
            tk.Label(frame, text=f"Баланс: {self.user[4]} руб.").pack(side=tk.LEFT, padx=5)
            tk.Button(frame, text="Пополнить", command=self.add_balance).pack(side=tk.LEFT, padx=5)

        elif self.user[3] == "admin":
            tk.Button(self.root, text="Добавить книгу", command=self.add_book).pack(pady=5)

        self.tree = ttk.Treeview(self.root, columns=("ID", "Title", "Author", "Category", "Price", "Quantity"),
                                 show='headings')

        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=0, stretch=tk.NO)  # Делаем невидимым

        self.tree.heading("Title", text="Название")
        self.tree.heading("Author", text="Автор")
        self.tree.heading("Category", text="Категория")
        self.tree.heading("Price", text="Цена")
        self.tree.heading("Quantity", text="Количество")

        self.tree.pack(fill=tk.BOTH, expand=True)

        if self.user[3] == "buyer":
            self.tree.bind("<Double-1>", self.buy_book)

        elif self.user[3] == "admin":
            self.tree.bind("<Double-1>", self.edit_book)

        self.load_books()

    def load_books(self):
        """ Функция загрузки информации о книгах из базы данных """
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("SELECT id, title, author, category, price, quantity FROM books")
        for row in self.cursor.fetchall():
            self.tree.insert("", tk.END, values=row)

    def add_balance(self):
        """ Функция пополнения баланса """
        amount = simpledialog.askfloat("Пополнение баланса", "Введите сумму пополнения:")
        if amount and amount > 0:
            new_balance = self.user[4] + amount
            self.cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, self.user[0]))
            self.conn.commit()
            self.user = (self.user[0], self.user[1], self.user[2], self.user[3], new_balance)
            messagebox.showinfo("Успех", f"Баланс пополнен. Новый баланс: {new_balance} руб.")
            self.show_main_interface()
        else:
            messagebox.showerror("Ошибка", "Введите корректную сумму.")

    def buy_book(self, event):
        """ Функция покупки книги """
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item[0])
        values = item['values']

        if len(values) != 6:  # Защита от ошибки
            messagebox.showerror("Ошибка", "Некорректные данные книги.")
            return

        book_id, title, author, category, price, quantity = values

        price = float(price)
        quantity = int(quantity)

        if quantity <= 0:
            messagebox.showerror("Ошибка", "Эта книга закончилась в наличии")
            return

        if self.user[4] < price:
            messagebox.showerror("Ошибка", "Недостаточно средств на балансе")
            return

        new_balance = self.user[4] - price
        new_quantity = quantity - 1

        self.cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, self.user[0]))
        self.cursor.execute("UPDATE books SET quantity = ? WHERE id = ?", (new_quantity, book_id))
        self.conn.commit()

        self.user = (self.user[0], self.user[1], self.user[2], self.user[3], new_balance)
        messagebox.showinfo("Успех", f"Вы купили '{title}' за {price} руб.")
        self.show_main_interface()

    def edit_book(self, event):
        """ Функция редактирования записи о книге """
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item[0])
        book_id, title, author, category, price, quantity = item['values']

        self.clear_window()
        frame = tk.Frame(self.root)
        frame.pack(expand=True)

        tk.Label(frame, text="Редактирование книги", font=("Arial", 16, "bold")).pack(pady=10)

        self.entry_title = tk.Entry(frame)
        self.entry_title.insert(0, title)
        self.entry_title.pack()

        self.entry_author = tk.Entry(frame)
        self.entry_author.insert(0, author)
        self.entry_author.pack()

        self.entry_category = tk.Entry(frame)
        self.entry_category.insert(0, category)
        self.entry_category.pack()

        self.entry_price = tk.Entry(frame)
        self.entry_price.insert(0, price)
        self.entry_price.pack()

        self.entry_quantity = tk.Entry(frame)
        self.entry_quantity.insert(0, quantity)
        self.entry_quantity.pack()

        tk.Button(frame, text="Сохранить", command=lambda: self.save_book(book_id)).pack(pady=5)
        tk.Button(frame, text="Удалить", command=lambda: self.delete_book(book_id)).pack(pady=5)
        tk.Button(frame, text="Назад", command=self.show_main_interface).pack(pady=5)

    def save_book(self, book_id):
        """ Функция сохранения измененной записи о книге """
        self.cursor.execute("UPDATE books SET title=?, author=?, category=?, price=?, quantity=? WHERE id=?",
                            (self.entry_title.get(), self.entry_author.get(), self.entry_category.get(),
                             float(self.entry_price.get()), int(self.entry_quantity.get()), book_id))
        self.conn.commit()
        self.show_main_interface()

    def delete_book(self, book_id):
        """ Функция удаления книги """
        self.cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
        self.conn.commit()
        self.show_main_interface()

    def add_book(self):
        """ Функция добавления книги """
        self.clear_window()
        frame = tk.Frame(self.root)
        frame.pack(expand=True)

        tk.Label(frame, text="Добавление книги", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(frame, text="Название").pack()
        self.entry_title = tk.Entry(frame)
        self.entry_title.pack()

        tk.Label(frame, text="Автор").pack()
        self.entry_author = tk.Entry(frame)
        self.entry_author.pack()

        tk.Label(frame, text="Категория").pack()
        self.entry_category = tk.Entry(frame)
        self.entry_category.pack()

        tk.Label(frame, text="Цена").pack()
        self.entry_price = tk.Entry(frame)
        self.entry_price.pack()

        tk.Label(frame, text="Количество").pack()
        self.entry_quantity = tk.Entry(frame)
        self.entry_quantity.pack()

        tk.Button(frame, text="Сохранить", command=self.save_new_book).pack(pady=5)
        tk.Button(frame, text="Назад", command=self.show_main_interface).pack(pady=5)

    def save_new_book(self):
        """ Функция добавления новой книги """
        try:
            price = float(self.entry_price.get())
            quantity = int(self.entry_quantity.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Цена и количество должны быть числами")
            return

        if not self.entry_title.get() or not self.entry_author.get() or not self.entry_category.get():
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return

        self.cursor.execute("INSERT INTO books (title, author, category, price, quantity) VALUES (?, ?, ?, ?, ?)",
                            (self.entry_title.get(), self.entry_author.get(), self.entry_category.get(), price,
                             quantity))
        self.conn.commit()
        self.show_main_interface()


if __name__ == "__main__":
    root = tk.Tk()
    app = BookstoreApp(root)
    init_db()
    root.mainloop()
