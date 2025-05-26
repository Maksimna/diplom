import sqlite3
from datetime import datetime

conn = sqlite3.connect("bookstore.db", timeout=10)
cur = conn.cursor()

# Удаление старых таблиц
cur.executescript("""
DROP TABLE IF EXISTS purchases;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS stock;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS books;
""")

# Создание таблиц
cur.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT DEFAULT 'Покупатель',
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
""")

cur.execute("""
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT,
    publisher TEXT,
    year INTEGER,
    isbn TEXT UNIQUE,
    purchase_price REAL,
    sale_price REAL,
    stock_quantity INTEGER,
    description TEXT
);
""")
cur.execute("""
                    CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        book_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL CHECK(quantity > 0),
                        price REAL NOT NULL,  -- цена за одну книгу на момент заказа
                        order_date TEXT DEFAULT (datetime('now')),
                        status TEXT DEFAULT 'в обработке',
                        FOREIGN KEY (user_id) REFERENCES users(id),
                        FOREIGN KEY (book_id) REFERENCES books(id)
                    );
                """)
cur.execute("""
CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT,
    phone TEXT,
    email TEXT
);
""")

cur.execute("""
CREATE TABLE suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT
);
""")

cur.execute("""
CREATE TABLE purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    supplier_id INTEGER,
    quantity INTEGER,
    purchase_price REAL,
    date TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(book_id) REFERENCES books(id),
    FOREIGN KEY(supplier_id) REFERENCES suppliers(id)
);
""")

cur.execute("""
CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    client_id INTEGER,
    user_id INTEGER,
    quantity INTEGER,
    discount REAL DEFAULT 0.0,
    total_price REAL,
    date TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(book_id) REFERENCES books(id),
    FOREIGN KEY(client_id) REFERENCES clients(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);
""")
cur.execute("""
CREATE TABLE supplies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    supplier_id INTEGER,
    quantity INTEGER,
    purchase_price REAL,
    supply_date TEXT,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);
""")
# Вставка тестовых данных
cur.executemany("INSERT INTO users (name, role, email, password) VALUES (?, ?, ?, ?);", [
    ("Иван Иванов", "Администратор", "ivan@example.com", "123456"),
    ("Мария Смирнова", "Покупатель", "maria@example.com", "abcdef"),
    ("Петр Петров", "Кассир", "petr@example.com", "qwerty")
])

cur.executemany("INSERT INTO books (title, author, genre, publisher, year, isbn, purchase_price, sale_price, stock_quantity, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", [
    ("1984", "Джордж Оруэлл", "Антиутопия", "Издательство 1", 1949, "9780141036144", 200.00, 350.00, 10, "Антиутопия о тоталитарном государстве"),
    ("Мастер и Маргарита", "Михаил Булгаков", "Фэнтези", "Издательство 2", 1966, "9785699449601", 250.00, 420.00, 7, "Роман о встрече дьявола с Москвой"),
    ("Преступление и наказание", "Ф. Достоевский", "Философия", "Издательство 3", 1866, "9780140449136", 230.00, 380.00, 5, "Философский роман о морали"),
    ("Война и мир", "Лев Толстой", "Исторический", "Издательство 4", 1869, "9780143039990", 300.00, 500.00, 3, "Эпопея о жизни в России"),
    ("Гарри Поттер", "Дж. К. Роулинг", "Фэнтези", "Bloomsbury", 1997, "9780747532743", 180.00, 300.00, 15, "Первая книга о Гарри Поттере")
])

cur.executemany("INSERT INTO clients (first_name, last_name, phone, email) VALUES (?, ?, ?, ?);", [
    ("Алексей", "Кузнецов", "+79031234567", "alexey@example.com"),
    ("Елена", "Новикова", "+79037654321", "elena@example.com")
])

cur.executemany("INSERT INTO suppliers (name, phone, email) VALUES (?, ?, ?);", [
    ("Поставщик №1", "+79035556677", "supply1@example.com"),
    ("Поставщик №2", "+79038889900", "supply2@example.com")
])

conn.commit()
conn.close()

print("База данных успешно создана и наполнена тестовыми данными.")
