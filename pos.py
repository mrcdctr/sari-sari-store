from inventory import InventoryManager
from tkinter import simpledialog
from datetime import datetime

class POS:
    def __init__(self):
        self.inventory = InventoryManager()
        self.cart = []
        self.user_id = None

    def set_user(self, user_id):
        self.user_id = user_id

    def scan_item(self, barcode, quantity=1):
        product = self.inventory.get_item_by_barcode(barcode)
        if product:
            if product[2] >= quantity:
                self.cart.append((product, quantity))
                return True, f"Added {quantity}x {product[1]} to cart (₱{product[3]*quantity:.2f})"
            return False, f"Insufficient stock for {product[1]} (Available: {product[2]})"
        return False, "Product not found - Barcode not recognized"

    def get_cart_total(self):
        return sum(item[0][3] * item[1] for item in self.cart)

    def checkout(self):
        if not self.cart:
            return False, "Cart is empty"
        
        total = self.get_cart_total()
        receipt = self.generate_receipt()
        for item, quantity in self.cart:
            self.inventory.db.record_sale(item[0], quantity, item[3] * quantity, self.user_id)
        self.cart.clear()
        with open(f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "w") as f:
            f.write(receipt)
        return True, f"Checkout successful. Total: ₱{total:.2f}\nReceipt saved."

    def generate_receipt(self):
        receipt = "Sari-Sari Store Receipt\n"
        receipt += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        receipt += "-------------------------\n"
        for item, qty in self.cart:
            receipt += f"{item[1]} x{qty}: ₱{item[3]*qty:.2f}\n"
        receipt += "-------------------------\n"
        receipt += f"Total: ₱{self.get_cart_total():.2f}\n"
        receipt += "Thank you for your purchase!\n"
        return receipt

    def clear_cart(self):
        self.cart.clear()

    def get_cart_items(self):
        return [(item[1], item[3], item[4], qty) for item, qty in self.cart]  # name, price, barcode, quantity