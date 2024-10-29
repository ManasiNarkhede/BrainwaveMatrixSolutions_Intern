import mysql.connector
from db_config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
from tkinter import messagebox

def connect_db():
    return mysql.connector.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        database=DB_NAME
    )

def register_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def login_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user is not None

def add_product(name, quantity, price):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COALESCE(MAX(id), 0) FROM products")
    max_id = cursor.fetchone()[0]
    
    new_id = max_id + 1
    
    cursor.execute("INSERT INTO products (id, name, quantity, price) VALUES (%s, %s, %s, %s)", 
                   (new_id, name, quantity, price))
    conn.commit()
    cursor.close()
    conn.close()

def update_product(product_id, name, quantity, price):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE products SET name = %s, quantity = %s, price = %s WHERE id = %s",
                       (name, quantity, price, product_id))
        conn.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def delete_product(product_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_products():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

def get_low_stock_products():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE quantity < %s", (5,))  # Replace 5 with your low stock threshold
    low_stock_products = cursor.fetchall()
    cursor.close()
    conn.close()
    return low_stock_products

# Sales functions
def add_sale(product_id, quantity_sold, price):
    total = quantity_sold * price
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sales (product_id, quantity_sold, price, total) VALUES (%s, %s, %s, %s)",
                   (product_id, quantity_sold, price, total))
    conn.commit()
    cursor.close()
    conn.close()

def update_sale(sale_id, quantity_sold):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT price FROM sales WHERE id = %s", (sale_id,))
    price = cursor.fetchone()[0]
    total = quantity_sold * price
    cursor.execute("UPDATE sales SET quantity_sold = %s, total = %s WHERE id = %s",
                   (quantity_sold, total, sale_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_sale(sale_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sales WHERE id = %s", (sale_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_sales():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales")
    sales = cursor.fetchall()
    cursor.close()
    conn.close()
    return sales
