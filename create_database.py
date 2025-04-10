import sqlite3
import datetime

def create_database():
    # Connect to the database (creates it if it doesn't exist)
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()

    # Create Products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        stock_quantity INTEGER NOT NULL,
        category TEXT NOT NULL
    )
    ''')

    # Create Customers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        address TEXT,
        registration_date TEXT NOT NULL
    )
    ''')

    # Create Orders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        order_date TEXT NOT NULL,
        total_amount REAL NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
    ''')

    # Create Order Items table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER NOT NULL,
        price_at_time REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
    ''')

    # Insert sample products
    products = [
        ('Laptop Pro', 'High-performance laptop with 16GB RAM', 1299.99, 50, 'Electronics'),
        ('Wireless Mouse', 'Ergonomic wireless mouse', 29.99, 100, 'Accessories'),
        ('Mechanical Keyboard', 'RGB mechanical keyboard', 89.99, 75, 'Accessories'),
        ('Smartphone X', 'Latest smartphone with 5G', 899.99, 30, 'Electronics'),
        ('Bluetooth Headphones', 'Noise-cancelling headphones', 199.99, 40, 'Audio'),
        ('Smart Watch', 'Fitness tracking smartwatch', 249.99, 60, 'Wearables'),
        ('External SSD', '1TB portable SSD', 149.99, 25, 'Storage'),
        ('Webcam HD', '1080p HD webcam', 79.99, 45, 'Accessories')
    ]
    cursor.executemany('''
    INSERT INTO products (name, description, price, stock_quantity, category)
    VALUES (?, ?, ?, ?, ?)
    ''', products)

    # Insert sample customers
    customers = [
        ('John', 'Doe', 'john.doe@email.com', '+1234567890', '123 Main St, City', '2024-01-15'),
        ('Jane', 'Smith', 'jane.smith@email.com', '+1987654321', '456 Oak Ave, Town', '2024-02-01'),
        ('Bob', 'Johnson', 'bob.johnson@email.com', '+1122334455', '789 Pine Rd, Village', '2024-02-15'),
        ('Alice', 'Williams', 'alice.w@email.com', '+1555666777', '321 Elm St, City', '2024-03-01')
    ]
    cursor.executemany('''
    INSERT INTO customers (first_name, last_name, email, phone, address, registration_date)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', customers)

    # Insert sample orders
    orders = [
        (1, '2024-03-10', 1299.99, 'Completed'),
        (2, '2024-03-11', 119.98, 'Processing'),
        (3, '2024-03-12', 899.99, 'Shipped'),
        (1, '2024-03-13', 199.99, 'Completed')
    ]
    cursor.executemany('''
    INSERT INTO orders (customer_id, order_date, total_amount, status)
    VALUES (?, ?, ?, ?)
    ''', orders)

    # Insert sample order items
    order_items = [
        (1, 1, 1, 1299.99),  # Laptop Pro
        (2, 2, 1, 29.99),    # Wireless Mouse
        (2, 3, 1, 89.99),    # Mechanical Keyboard
        (3, 4, 1, 899.99),   # Smartphone X
        (4, 5, 1, 199.99)    # Bluetooth Headphones
    ]
    cursor.executemany('''
    INSERT INTO order_items (order_id, product_id, quantity, price_at_time)
    VALUES (?, ?, ?, ?)
    ''', order_items)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Database created successfully with sample data!") 