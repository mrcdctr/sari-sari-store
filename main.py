import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from ttkthemes import ThemedTk  # For modern theme
from inventory import InventoryManager
from pos import POS
from reports import ReportGenerator
from analytics import InventoryAnalytics
from supply_chain import SupplyChainManager
from login import LoginWindow
from datetime import datetime
import cv2
from pyzbar.pyzbar import decode
import winsound  # For sound feedback (Windows-specific; use alternatives for other OS)
import requests  # For mobile phone camera stream
import numpy as np

class SariSariStoreApp:
    def __init__(self, root):
        self.root = ThemedTk(theme="arc")  # Modern theme
        self.root.title("Sari-Sari Store System - Login")
        self.root.geometry("300x200")
        self.user_id = None
        self.root.option_add("*Font", "Helvetica 14 bold")  # Default bigger, bold font
        print("Initializing LoginWindow")
        try:
            LoginWindow(self.root, self.start_main_app)
        except Exception as e:
            print(f"Error initializing LoginWindow: {str(e)}")
            messagebox.showerror("Error", f"Initialization failed: {str(e)}")

    def start_main_app(self, user_id):
        print(f"Starting main app with user_id: {user_id}")
        self.user_id = user_id
        try:
            self.root.title("Sari-Sari Store System")
            self.root.geometry("1200x800")  # Larger window for modern look
            self.root.configure(bg="#f0f0f0")  # Light gray background
            self.inventory = InventoryManager()
            self.pos = POS()
            self.pos.set_user(user_id)
            self.reports = ReportGenerator()
            self.analytics = InventoryAnalytics()
            self.supply = SupplyChainManager()
            print("Managers initialized")
            self.create_widgets()
            print("Main app UI setup complete")
            self.root.update()
        except Exception as e:
            print(f"Error in start_main_app: {str(e)}")
            messagebox.showerror("Error", f"Failed to initialize main app: {str(e)}")

    def create_widgets(self):
        print("Entering create_widgets")
        try:
            style = ttk.Style()
            style.configure("TNotebook", background="#f0f0f0", font=("Helvetica", 16, "bold"))
            style.configure("TNotebook.Tab", padding=[10, 5], font=("Helvetica", 14, "bold"))
            style.configure("TButton", padding=10, font=("Helvetica", 14, "bold"))
            style.configure("TLabel", font=("Helvetica", 14, "bold"))
            style.configure("TEntry", font=("Helvetica", 14))

            notebook = ttk.Notebook(self.root)
            notebook.pack(pady=20, padx=20, expand=True, fill="both")
            print("Notebook created")

            inventory_frame = ttk.Frame(notebook, padding=20)
            notebook.add(inventory_frame, text="Inventory")
            self.create_inventory_widgets(inventory_frame)

            pos_frame = ttk.Frame(notebook, padding=20)
            notebook.add(pos_frame, text="Point of Sale")
            self.create_pos_widgets(pos_frame)

            reports_frame = ttk.Frame(notebook, padding=20)
            notebook.add(reports_frame, text="Reports")
            self.create_reports_widgets(reports_frame)

            analytics_frame = ttk.Frame(notebook, padding=20)
            notebook.add(analytics_frame, text="Analytics")
            self.create_analytics_widgets(analytics_frame)

            supply_frame = ttk.Frame(notebook, padding=20)
            notebook.add(supply_frame, text="Supply Chain")
            self.create_supply_widgets(supply_frame)

            print("All widgets created successfully")
        except Exception as e:
            print(f"Error in create_widgets: {str(e)}")
            messagebox.showerror("Error", f"Widget creation failed: {str(e)}")

    def create_pos_widgets(self, frame):
        scan_frame = ttk.Frame(frame, padding="10")
        scan_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(scan_frame, text="Scan Barcode/QR:").grid(row=0, column=0, padx=10, pady=10)
        self.scan_entry = ttk.Entry(scan_frame, width=30)
        self.scan_entry.grid(row=0, column=1, padx=10, pady=10)
        self.scan_entry.bind("<Return>", self.scan_product)

        ttk.Button(scan_frame, text="Scan", command=self.scan_product).grid(row=0, column=2, padx=10, pady=10)
        ttk.Button(scan_frame, text="Camera Scan", command=self.start_continuous_camera_scan).grid(row=0, column=3, padx=10, pady=10)
        ttk.Button(scan_frame, text="Mobile Scan", command=self.start_mobile_scan).grid(row=0, column=4, padx=10, pady=10)

        self.cart_tree = ttk.Treeview(frame, columns=("Name", "Price", "Barcode", "Quantity"), show="headings", height=15)
        self.cart_tree.grid(row=1, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))
        self.cart_tree.heading("Name", text="Product Name")
        self.cart_tree.heading("Price", text="Price")
        self.cart_tree.heading("Barcode", text="Barcode")
        self.cart_tree.heading("Quantity", text="Quantity")
        self.cart_tree.column("Name", width=300)
        self.cart_tree.column("Price", width=150)
        self.cart_tree.column("Barcode", width=200)
        self.cart_tree.column("Quantity", width=100)

        self.total_label = ttk.Label(frame, text="Total: ₱0.00")
        self.total_label.grid(row=2, column=0, pady=10)
        ttk.Button(frame, text="Checkout", command=self.checkout).grid(row=3, column=0, pady=10)
        ttk.Button(frame, text="Clear Cart", command=self.clear_cart).grid(row=4, column=0, pady=10)

        ttk.Label(frame, text="Scanner Options: USB/Bluetooth, Webcam, or Mobile Camera").grid(row=5, column=0, pady=10)

    def scan_product(self, event=None):
        barcode_input = self.scan_entry.get().strip()
        if not barcode_input:
            messagebox.showerror("Error", "Please enter or scan a barcode")
            return
        barcode, quantity = self.parse_barcode(barcode_input)
        success, message = self.pos.scan_item(barcode, quantity)
        if success:
            winsound.Beep(1000, 200)  # Beep sound (frequency: 1000 Hz, duration: 200 ms)
            self.refresh_cart()
            self.scan_entry.delete(0, tk.END)
        messagebox.showinfo("Scan Result", message)

    def start_continuous_camera_scan(self):
        self.scan_window = tk.Toplevel(self.root)
        self.scan_window.title("Continuous Barcode Scanner")
        self.scan_window.geometry("640x480")
        self.scan_window.attributes("-topmost", True)

        self.canvas = tk.Canvas(self.scan_window, width=640, height=480)
        self.canvas.pack()
        ttk.Button(self.scan_window, text="Stop Scanning", command=self.stop_camera_scan).pack(pady=10)

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not access webcam")
            self.scan_window.destroy()
            return
        self.scanning = True
        self.update_camera_feed()

    def stop_camera_scan(self):
        self.scanning = False
        if self.cap:
            self.cap.release()
        self.scan_window.destroy()

    def update_camera_feed(self):
        if self.scanning:
            ret, frame = self.cap.read()
            if ret:
                barcodes = decode(frame)
                if barcodes:
                    barcode = barcodes[0].data.decode('utf-8')
                    barcode, quantity = self.parse_barcode(barcode)
                    success, message = self.pos.scan_item(barcode, quantity)
                    if success:
                        winsound.Beep(1000, 200)
                        self.refresh_cart()
                        messagebox.showinfo("Scan Result", message)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = tk.PhotoImage(data=cv2.imencode('.ppm', frame)[1].tobytes())
                self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
                self.canvas.image = img  # Keep reference to avoid garbage collection

            self.scan_window.after(50, self.update_camera_feed)  # Update every 50ms

    def start_mobile_scan(self):
        mobile_url = simpledialog.askstring("Mobile Camera", "Enter IP Webcam URL (e.g., http://192.168.1.100:8080/shot.jpg):")
        if not mobile_url:
            return
        self.scan_window = tk.Toplevel(self.root)
        self.scan_window.title("Mobile Barcode Scanner")
        self.scan_window.geometry("640x480")
        self.scan_window.attributes("-topmost", True)

        self.canvas = tk.Canvas(self.scan_window, width=640, height=480)
        self.canvas.pack()
        ttk.Button(self.scan_window, text="Stop Scanning", command=self.stop_mobile_scan).pack(pady=10)

        self.mobile_url = mobile_url
        self.scanning = True
        self.update_mobile_feed()

    def stop_mobile_scan(self):
        self.scanning = False
        self.scan_window.destroy()

    def update_mobile_feed(self):
        if self.scanning:
            try:
                response = requests.get(self.mobile_url, timeout=5)
                img_array = np.array(bytearray(response.content), dtype=np.uint8)
                frame = cv2.imdecode(img_array, -1)
                barcodes = decode(frame)
                if barcodes:
                    barcode = barcodes[0].data.decode('utf-8')
                    barcode, quantity = self.parse_barcode(barcode)
                    success, message = self.pos.scan_item(barcode, quantity)
                    if success:
                        winsound.Beep(1000, 200)
                        self.refresh_cart()
                        messagebox.showinfo("Scan Result", message)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = tk.PhotoImage(data=cv2.imencode('.ppm', frame)[1].tobytes())
                self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
                self.canvas.image = img
            except Exception as e:
                print(f"Mobile scan error: {str(e)}")
                messagebox.showerror("Error", f"Mobile scan failed: {str(e)}")
                self.stop_mobile_scan()
                return

            self.scan_window.after(50, self.update_mobile_feed)

    def parse_barcode(self, barcode_data):
        # QR code format: "barcode:quantity" (e.g., "123456789012:2")
        if ":" in barcode_data:
            try:
                barcode, quantity = barcode_data.split(":")
                return barcode.strip(), int(quantity)
            except ValueError:
                return barcode_data, 1  # Fallback to quantity 1 if parsing fails
        return barcode_data, simpledialog.askinteger("Quantity", "Enter quantity:", minvalue=1, initialvalue=1) or 1

    def refresh_cart(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        for name, price, barcode, qty in self.pos.get_cart_items():
            self.cart_tree.insert("", "end", values=(name, f"₱{price:.2f}", barcode, qty))
        self.total_label.config(text=f"Total: ₱{self.pos.get_cart_total():.2f}")

    def checkout(self):
        success, message = self.pos.checkout()
        if success:
            self.refresh_cart()
            self.refresh_inventory()
        messagebox.showinfo("Result", message)

    def clear_cart(self):
        self.pos.clear_cart()
        self.refresh_cart()

    # Other widget creation methods (unchanged for brevity but styled similarly)
    def create_inventory_widgets(self, frame):
        input_frame = ttk.Frame(frame, padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        ttk.Label(input_frame, text="Product Name:").grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = ttk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(input_frame, text="Quantity:").grid(row=1, column=0, padx=10, pady=10)
        self.quantity_entry = ttk.Entry(input_frame, width=30)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(input_frame, text="Price:").grid(row=2, column=0, padx=10, pady=10)
        self.price_entry = ttk.Entry(input_frame, width=30)
        self.price_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(input_frame, text="Barcode:").grid(row=3, column=0, padx=10, pady=10)
        self.barcode_entry = ttk.Entry(input_frame, width=30)
        self.barcode_entry.grid(row=3, column=1, padx=10, pady=10)

        ttk.Label(input_frame, text="Supplier:").grid(row=4, column=0, padx=10, pady=10)
        self.supplier_combo = ttk.Combobox(input_frame, width=28)
        self.supplier_combo.grid(row=4, column=1, padx=10, pady=10)
        self.update_supplier_combo()

        ttk.Button(input_frame, text="Add Product", command=self.add_product).grid(row=5, column=0, pady=10)
        ttk.Button(input_frame, text="Update Product", command=self.update_product).grid(row=5, column=1, pady=10)
        ttk.Button(input_frame, text="Delete Product", command=self.delete_product).grid(row=5, column=2, pady=10)
        ttk.Button(input_frame, text="View Transactions", command=self.show_transactions).grid(row=5, column=3, pady=10)

        self.tree = ttk.Treeview(frame, columns=("ID", "Name", "Quantity", "Price", "Barcode", "Supplier"), show="headings", height=15)
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Product Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Barcode", text="Barcode")
        self.tree.heading("Supplier", text="Supplier")
        self.tree.column("ID", width=50)
        self.tree.column("Name", width=200)
        self.tree.column("Quantity", width=100)
        self.tree.column("Price", width=100)
        self.tree.column("Barcode", width=150)
        self.tree.column("Supplier", width=200)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.refresh_inventory()

        self.transaction_text = tk.Text(frame, height=10, width=80, font=("Helvetica", 14))
        self.transaction_text.grid(row=2, column=0, padx=10, pady=10)

    def create_reports_widgets(self, frame):
        date_frame = ttk.Frame(frame, padding="10")
        date_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        ttk.Label(date_frame, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)
        self.start_date = ttk.Entry(date_frame, width=30)
        self.start_date.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(date_frame, text="End Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=10)
        self.end_date = ttk.Entry(date_frame, width=30)
        self.end_date.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(date_frame, text="Generate Report", command=self.generate_report).grid(row=2, column=0, pady=10)

        self.report_text = tk.Text(frame, height=20, width=80, font=("Helvetica", 14))
        self.report_text.grid(row=1, column=0, padx=10, pady=10)

    def create_analytics_widgets(self, frame):
        analytics_frame = ttk.Frame(frame, padding="10")
        analytics_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        ttk.Button(analytics_frame, text="Low Stock Alert", command=self.show_low_stock).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(analytics_frame, text="Sales Trend", command=self.show_sales_trend).grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(analytics_frame, text="Top Products", command=self.show_top_products).grid(row=0, column=2, padx=10, pady=10)
        
        ttk.Label(analytics_frame, text="Forecast Method:").grid(row=1, column=0, padx=10, pady=10)
        self.forecast_method = ttk.Combobox(analytics_frame, values=["sma", "exp", "lr"], width=28)
        self.forecast_method.set("sma")
        self.forecast_method.grid(row=1, column=1, padx=10, pady=10)
        ttk.Button(analytics_frame, text="Forecast Sales", command=self.show_forecast).grid(row=1, column=2, padx=10, pady=10)
        
        ttk.Button(analytics_frame, text="Optimize Inventory", command=self.show_optimization).grid(row=2, column=0, padx=10, pady=10)
        ttk.Button(analytics_frame, text="Plot Sales Trend", command=self.plot_sales_trend).grid(row=2, column=1, padx=10, pady=10)
        ttk.Button(analytics_frame, text="Plot Top Products", command=self.plot_top_products).grid(row=2, column=2, padx=10, pady=10)
        ttk.Button(analytics_frame, text="Plot Forecast", command=self.plot_forecast).grid(row=2, column=3, padx=10, pady=10)

        self.analytics_text = tk.Text(frame, height=20, width=80, font=("Helvetica", 14))
        self.analytics_text.grid(row=1, column=0, padx=10, pady=10)

    def create_supply_widgets(self, frame):
        supplier_frame = ttk.Frame(frame, padding="10")
        supplier_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        ttk.Label(supplier_frame, text="Supplier Name:").grid(row=0, column=0, padx=10, pady=10)
        self.supplier_name = ttk.Entry(supplier_frame, width=30)
        self.supplier_name.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(supplier_frame, text="Contact:").grid(row=1, column=0, padx=10, pady=10)
        self.supplier_contact = ttk.Entry(supplier_frame, width=30)
        self.supplier_contact.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(supplier_frame, text="Lead Time (days):").grid(row=2, column=0, padx=10, pady=10)
        self.supplier_lead = ttk.Entry(supplier_frame, width=30)
        self.supplier_lead.grid(row=2, column=1, padx=10, pady=10)

        ttk.Button(supplier_frame, text="Add Supplier", command=self.add_supplier).grid(row=3, column=0, pady=10)
        ttk.Button(supplier_frame, text="Update Supplier", command=self.update_supplier).grid(row=3, column=1, pady=10)
        ttk.Button(supplier_frame, text="Delete Supplier", command=self.delete_supplier).grid(row=3, column=2, pady=10)
        ttk.Button(supplier_frame, text="Reorder Recommendation", command=self.show_reorder).grid(row=3, column=3, pady=10)

        self.supplier_tree = ttk.Treeview(frame, columns=("ID", "Name", "Contact", "LeadTime"), show="headings", height=15)
        self.supplier_tree.grid(row=1, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))
        self.supplier_tree.heading("ID", text="ID")
        self.supplier_tree.heading("Name", text="Name")
        self.supplier_tree.heading("Contact", text="Contact")
        self.supplier_tree.heading("LeadTime", text="Lead Time")
        self.supplier_tree.column("ID", width=50)
        self.supplier_tree.column("Name", width=200)
        self.supplier_tree.column("Contact", width=300)
        self.supplier_tree.column("LeadTime", width=150)
        self.supplier_tree.bind("<<TreeviewSelect>>", self.on_supplier_select)
        self.refresh_suppliers()

        self.supply_text = tk.Text(frame, height=15, width=80, font=("Helvetica", 14))
        self.supply_text.grid(row=2, column=0, padx=10, pady=10)

    def refresh_inventory(self):
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            for product in self.inventory.get_items():
                self.tree.insert("", "end", values=product)
        except Exception as e:
            print(f"Error in refresh_inventory: {str(e)}")
            messagebox.showerror("Error", f"Failed to refresh inventory: {str(e)}")

    def refresh_suppliers(self):
        try:
            for item in self.supplier_tree.get_children():
                self.supplier_tree.delete(item)
            for supplier in self.supply.get_suppliers():
                self.supplier_tree.insert("", "end", values=supplier)
        except Exception as e:
            print(f"Error in refresh_suppliers: {str(e)}")
            messagebox.showerror("Error", f"Failed to refresh suppliers: {str(e)}")

    def update_supplier_combo(self):
        try:
            suppliers = self.supply.get_suppliers()
            self.supplier_combo['values'] = [f"{s[0]}: {s[1]}" for s in suppliers]
            self.supplier_combo.set("")
        except Exception as e:
            print(f"Error in update_supplier_combo: {str(e)}")
            messagebox.showerror("Error", f"Failed to update supplier combo: {str(e)}")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.barcode_entry.delete(0, tk.END)
        self.supplier_combo.set("")

    def clear_supplier_entries(self):
        self.supplier_name.delete(0, tk.END)
        self.supplier_contact.delete(0, tk.END)
        self.supplier_lead.delete(0, tk.END)

    def add_product(self):
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()
        barcode = self.barcode_entry.get()
        supplier = self.supplier_combo.get()
        supplier_id = int(supplier.split(":")[0]) if supplier else None

        if not all([name, quantity, price, barcode]):
            messagebox.showerror("Error", "All fields except supplier are required")
            return

        success, message = self.inventory.add_item(name, quantity, price, barcode, supplier_id, self.user_id)
        if success:
            self.refresh_inventory()
            self.clear_entries()
        messagebox.showinfo("Result", message)

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            values = item['values']
            self.clear_entries()
            self.name_entry.insert(0, values[1])
            self.quantity_entry.insert(0, values[2])
            self.price_entry.insert(0, values[3])
            self.barcode_entry.insert(0, values[4])
            self.supplier_combo.set(values[5] if values[5] else "")

    def update_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a product to update")
            return

        product_id = self.tree.item(selected_item)['values'][0]
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()
        barcode = self.barcode_entry.get()
        supplier = self.supplier_combo.get()
        supplier_id = int(supplier.split(":")[0]) if supplier else None

        if not all([name, quantity, price, barcode]):
            messagebox.showerror("Error", "All fields except supplier are required")
            return

        success, message = self.inventory.update_item(product_id, name, quantity, price, barcode, supplier_id, self.user_id)
        if success:
            self.refresh_inventory()
            self.clear_entries()
        messagebox.showinfo("Result", message)

    def delete_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a product to delete")
            return

        product_id = self.tree.item(selected_item)['values'][0]
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this product?"):
            success, message = self.inventory.delete_item(product_id, self.user_id)
            if success:
                self.refresh_inventory()
                self.clear_entries()
            messagebox.showinfo("Result", message)

    def show_transactions(self):
        selected_item = self.tree.selection()
        if not selected_item:
            transactions = self.inventory.get_transaction_history()
            report = "All Inventory Transactions\n-------------------------\n"
            if not transactions:
                report += "No transactions recorded"
            for t in transactions:
                report += f"Product: {t[6]}\nChange: {t[2]}\nAction: {t[3]}\nDate: {t[4]}\nUser: {t[7] if t[7] else 'Unknown'}\n\n"
        else:
            product_id = self.tree.item(selected_item)['values'][0]
            transactions = self.inventory.get_transaction_history(product_id)
            report = f"Transactions for Product ID {product_id}\n-------------------------\n"
            if not transactions:
                report += "No transactions recorded"
            for t in transactions:
                report += f"Change: {t[2]}\nAction: {t[3]}\nDate: {t[4]}\nUser: {t[5] if t[5] else 'Unknown'}\n\n"
        self.transaction_text.delete(1.0, tk.END)
        self.transaction_text.insert(tk.END, report)

    def generate_report(self):
        start_date = self.start_date.get()
        end_date = self.end_date.get()
        
        if not all([start_date, end_date]):
            messagebox.showerror("Error", "Please enter both dates")
            return

        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
            return

        report = self.reports.generate_sales_report(start_date, end_date)
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, report)

    def show_low_stock(self):
        report = self.analytics.get_low_stock_alert()
        self.analytics_text.delete(1.0, tk.END)
        self.analytics_text.insert(tk.END, report)

    def show_sales_trend(self):
        report = self.analytics.get_sales_trend_analysis()
        self.analytics_text.delete(1.0, tk.END)
        self.analytics_text.insert(tk.END, report)

    def show_top_products(self):
        report = self.analytics.get_product_performance()
        self.analytics_text.delete(1.0, tk.END)
        self.analytics_text.insert(tk.END, report)

    def show_forecast(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a product from Inventory tab first")
            return
        
        try:
            product_id = int(self.tree.item(selected_item)['values'][0])
            method = self.forecast_method.get()
            report = self.analytics.forecast_sales(product_id, method=method)
            self.analytics_text.delete(1.0, tk.END)
            self.analytics_text.insert(tk.END, report)
        except Exception as e:
            messagebox.showerror("Error", f"Forecasting failed: {str(e)}")

    def show_optimization(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a product from Inventory tab first")
            return
        
        try:
            product_id = int(self.tree.item(selected_item)['values'][0])
            report = self.analytics.optimize_inventory(product_id)
            self.analytics_text.delete(1.0, tk.END)
            self.analytics_text.insert(tk.END, report)
        except Exception as e:
            messagebox.showerror("Error", f"Optimization failed: {str(e)}")

    def plot_sales_trend(self):
        self.analytics.plot_sales_trend()

    def plot_top_products(self):
        self.analytics.plot_top_products()

    def plot_forecast(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a product from Inventory tab first")
            return
        product_id = int(self.tree.item(selected_item)['values'][0])
        method = self.forecast_method.get()
        self.analytics.plot_forecast(product_id, method=method)

    def add_supplier(self):
        name = self.supplier_name.get()
        contact = self.supplier_contact.get()
        lead_time = self.supplier_lead.get()

        if not all([name, contact, lead_time]):
            messagebox.showerror("Error", "All fields are required")
            return

        success, message = self.supply.add_supplier(name, contact, lead_time)
        if success:
            self.refresh_suppliers()
            self.update_supplier_combo()
            self.clear_supplier_entries()
        messagebox.showinfo("Result", message)

    def on_supplier_select(self, event):
        selected_item = self.supplier_tree.selection()
        if selected_item:
            item = self.supplier_tree.item(selected_item)
            values = item['values']
            self.clear_supplier_entries()
            self.supplier_name.insert(0, values[1])
            self.supplier_contact.insert(0, values[2])
            self.supplier_lead.insert(0, values[3])

    def update_supplier(self):
        selected_item = self.supplier_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a supplier to update")
            return

        supplier_id = self.supplier_tree.item(selected_item)['values'][0]
        name = self.supplier_name.get()
        contact = self.supplier_contact.get()
        lead_time = self.supplier_lead.get()

        if not all([name, contact, lead_time]):
            messagebox.showerror("Error", "All fields are required")
            return

        success, message = self.supply.update_supplier(supplier_id, name, contact, lead_time)
        if success:
            self.refresh_suppliers()
            self.update_supplier_combo()
            self.clear_supplier_entries()
        messagebox.showinfo("Result", message)

    def delete_supplier(self):
        selected_item = self.supplier_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a supplier to delete")
            return

        supplier_id = self.supplier_tree.item(selected_item)['values'][0]
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this supplier?"):
            success, message = self.supply.delete_supplier(supplier_id)
            if success:
                self.refresh_suppliers()
                self.update_supplier_combo()
                self.clear_supplier_entries()
            messagebox.showinfo("Result", message)

    def show_reorder(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a product from Inventory tab first")
            return
        
        product = self.tree.item(selected_item)['values']
        report = self.supply.get_reorder_recommendation(product)
        self.supply_text.delete(1.0, tk.END)
        self.supply_text.insert(tk.END, report)

if __name__ == "__main__":
    root = tk.Tk()
    app = SariSariStoreApp(root)
    print("Starting Tkinter mainloop")
    try:
        root.mainloop()
    except Exception as e:
        print(f"Error in mainloop: {str(e)}")