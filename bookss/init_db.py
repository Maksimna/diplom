import sqlite3
from datetime import datetime

# Установка соединения с тайм-аутом (для избежания "database is locked")
conn = sqlite3.connect("bookstore.db", timeout=10)
cur = conn.cursor()

# Удаление старых таблиц
cur.executescript("""
DROP TABLE IF EXISTS favorites;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS users;
""")

# Создание таблиц
cur.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
""")

cur.execute("""
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    description TEXT,
    price REAL,
    stock INTEGER
);
""")

cur.execute("""
CREATE TABLE favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(book_id) REFERENCES books(id),
    UNIQUE(user_id, book_id)
);
""")

cur.execute("""
CREATE TABLE orders (
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

# Вставка тестовых пользователей
users = [
    ("Иван Иванов", "ivan@example.com", "123456"),
    ("Мария Смирнова", "maria@example.com", "abcdef"),
    ("Петр Петров", "petr@example.com", "qwerty")
]
cur.executemany("INSERT INTO users (name, email, password) VALUES (?, ?, ?);", users)

# Вставка тестовых книг
books = [
    ("1984", "Джордж Оруэлл", "Антиутопия о тоталитарном государстве", 350.00, 10),
    ("Мастер и Маргарита", "Михаил Булгаков", "Роман о встрече дьявола с Москвой", 420.00, 7),
    ("Преступление и наказание", "Фёдор Достоевский", "Философский роман о морали и преступлении", 380.00, 5),
    ("Война и мир", "Лев Толстой", "Эпопея о жизни в России во времена Наполеона", 500.00, 3),
    ("Гарри Поттер и философский камень", "Дж. К. Роулинг", "Первая книга о Гарри Поттере", 300.00, 15)
]
cur.executemany("INSERT INTO books (title, author, description, price, stock) VALUES (?, ?, ?, ?, ?);", books)

conn.commit()
conn.close()

print("База данных успешно создана и наполнена тестовыми данными.")
