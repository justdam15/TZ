import sqlite3
import csv
import os

# Функция для выполнения SQL-запросов и сохранения результатов в CSV
def execute_query_and_save_to_csv(query, conn, output_file):
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    headers = [description[0] for description in cursor.description]
    
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)
        
    print(f'Results written to {output_file}')

# Создание соединения с базой данных SQLite
conn = sqlite3.connect('shop.db')

# Создание папки для сохранения результатов
output_folder = 'output'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Определение запросов
queries = {
    'total_cost_per_order': '''
    SELECT
        od.order_id,
        SUM(od.quantity * p.price) AS total_cost
    FROM
        Order_Details od
    JOIN
        Products p ON od.product_id = p.product_id
    GROUP BY
        od.order_id
    ORDER BY
        od.order_id
    ''',
    'average_price_per_order': '''
    SELECT
        od.order_id,
        AVG(p.price) AS average_price
    FROM
        Order_Details od
    JOIN
        Products p ON od.product_id = p.product_id
    GROUP BY
        od.order_id
    ORDER BY
        od.order_id
    ''',
    'total_cost_all_orders': '''
    SELECT
        SUM(od.quantity * p.price) AS total_cost
    FROM
        Order_Details od
    JOIN
        Products p ON od.product_id = p.product_id
    '''
}

# Выполнение запросов и сохранение результатов
execute_query_and_save_to_csv(queries['total_cost_per_order'], conn, os.path.join(output_folder, 'total_cost_per_order.csv'))
execute_query_and_save_to_csv(queries['average_price_per_order'], conn, os.path.join(output_folder, 'average_price_per_order.csv'))
execute_query_and_save_to_csv(queries['total_cost_all_orders'], conn, os.path.join(output_folder, 'total_cost_all_orders.csv'))

# Закрытие соединения с базой данных
conn.close()
