import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('inventory.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.migrate_schema()  # Add schema migration

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                barcode TEXT UNIQUE,
                supplier_id INTEGER,
                FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                quantity INTEGER,
                total REAL,
                sale_date TEXT,
                FOREIGN KEY (product_id) REFERENCES inventory(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact TEXT,
                lead_time INTEGER
            )
        ''')
        self.conn.commit()

    def migrate_schema(self):
        # Check if supplier_id column exists in inventory table
        self.cursor.execute("PRAGMA table_info(inventory)")
        columns = [col[1] for col in self.cursor.fetchall()]
        if 'supplier_id' not in columns:
            self.cursor.execute('ALTER TABLE inventory ADD COLUMN supplier_id INTEGER')
            self.conn.commit()
            print("Added supplier_id column to inventory table")

    def add_product(self, name, quantity, price, barcode, supplier_id=None):
        self.cursor.execute('INSERT INTO inventory (product_name, quantity, price, barcode, supplier_id) VALUES (?, ?, ?, ?, ?)',
                           (name, quantity, price, barcode, supplier_id))
        self.conn.commit()

    def get_all_products(self):
        self.cursor.execute('SELECT i.*, s.name FROM inventory i LEFT JOIN suppliers s ON i.supplier_id = s.id')
        return self.cursor.fetchall()

    def get_product_by_barcode(self, barcode):
        self.cursor.execute('SELECT * FROM inventory WHERE barcode = ?', (barcode,))
        return self.cursor.fetchone()

    def update_product(self, product_id, name, quantity, price, barcode, supplier_id=None):
        self.cursor.execute('UPDATE inventory SET product_name=?, quantity=?, price=?, barcode=?, supplier_id=? WHERE id=?',
                           (name, quantity, price, barcode, supplier_id, product_id))
        self.conn.commit()

    def delete_product(self, product_id):
        self.cursor.execute('DELETE FROM inventory WHERE id=?', (product_id,))
        self.conn.commit()

    def record_sale(self, product_id, quantity, total):
        sale_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('INSERT INTO sales (product_id, quantity, total, sale_date) VALUES (?, ?, ?, ?)',
                           (product_id, quantity, total, sale_date))
        self.cursor.execute('UPDATE inventory SET quantity = quantity - ? WHERE id = ?', (quantity, product_id))
        self.conn.commit()

    def get_sales_report(self, start_date, end_date):
        self.cursor.execute('''
            SELECT i.product_name, SUM(s.quantity), SUM(s.total), s.sale_date 
            FROM sales s 
            JOIN inventory i ON s.product_id = i.id 
            WHERE s.sale_date BETWEEN ? AND ?
            GROUP BY i.product_name, s.sale_date
        ''', (start_date, end_date))
        return self.cursor.fetchall()

    def get_low_stock_products(self, threshold=10):
        self.cursor.execute('SELECT * FROM inventory WHERE quantity <= ?', (threshold,))
        return self.cursor.fetchall()

    def get_sales_trend(self, days=30):
        self.cursor.execute('''
            SELECT DATE(sale_date), SUM(quantity), SUM(total)
            FROM sales
            WHERE sale_date >= datetime('now', ?)
            GROUP BY DATE(sale_date)
            ORDER BY DATE(sale_date)
        ''', (f'-{days} days',))
        return self.cursor.fetchall()

    def get_top_products(self, limit=5):
        self.cursor.execute('''
            SELECT i.product_name, SUM(s.quantity), SUM(s.total)
            FROM sales s
            JOIN inventory i ON s.product_id = i.id
            GROUP BY i.product_name
            ORDER BY SUM(s.quantity) DESC
            LIMIT ?
        ''', (limit,))
        return self.cursor.fetchall()

    def get_sales_history(self, product_id, days=30):
        self.cursor.execute('''
            SELECT DATE(sale_date), SUM(quantity)
            FROM sales
            WHERE product_id = ? AND sale_date >= datetime('now', ?)
            GROUP BY DATE(sale_date)
            ORDER BY DATE(sale_date)
        ''', (product_id, f'-{days} days'))
        return self.cursor.fetchall()

    def add_supplier(self, name, contact, lead_time):
        self.cursor.execute('INSERT INTO suppliers (name, contact, lead_time) VALUES (?, ?, ?)',
                           (name, contact, lead_time))
        self.conn.commit()

    def get_all_suppliers(self):
        self.cursor.execute('SELECT * FROM suppliers')
        return self.cursor.fetchall()

    def update_supplier(self, supplier_id, name, contact, lead_time):
        self.cursor.execute('UPDATE suppliers SET name=?, contact=?, lead_time=? WHERE id=?',
                           (name, contact, lead_time, supplier_id))
        self.conn.commit()

    def delete_supplier(self, supplier_id):
        self.cursor.execute('DELETE')