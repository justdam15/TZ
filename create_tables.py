import sqlite3

# Создание соединения с базой данных SQLite
conn = sqlite3.connect('shop.db')
cursor = conn.cursor()

# Создание таблицы Products
cursor.execute('''
CREATE TABLE IF NOT EXISTS Products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL
)
''')

# Создание таблицы Orders
cursor.execute('''
CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    order_date DATE NOT NULL
)
''')

# Создание таблицы Order_Details
cursor.execute('''
CREATE TABLE IF NOT EXISTS Order_Details (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders (order_id),
    FOREIGN KEY (product_id) REFERENCES Products (product_id),
    PRIMARY KEY (order_id, product_id)
)
''')

# Вставка тестовых данных в таблицу Products
cursor.executemany('INSERT INTO Products (name, price) VALUES (?, ?)', [
    ('Product1', 10.0),
    ('Product2', 20.0),
    ('Product3', 30.0)
])

# Вставка тестовых данных в таблицу Orders
cursor.executemany('INSERT INTO Orders (customer_name, order_date) VALUES (?, ?)', [
    ('Alice', '2023-07-01'),
    ('Bob', '2023-07-02')
])

# Вставка тестовых данных в таблицу Order_Details
cursor.executemany('INSERT INTO Order_Details (order_id, product_id, quantity) VALUES (?, ?, ?)', [
    (1, 1, 2),
    (1, 2, 3),
    (2, 3, 1)
])

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
