from inventory import InventoryManager

class POS:
    def __init__(self):
        self.inventory = InventoryManager()
        self.cart = []

    def scan_item(self, barcode):
        product = self.inventory.get_item_by_barcode(barcode)
        if product:
            if product[2] > 0:  # Check if quantity > 0
                self.cart.append(product)
                return True, f"Added {product[1]} to cart (₱{product[3]:.2f})"
            return False, f"{product[1]} is out of stock"
        return False, "Product not found - Barcode not recognized"

    def get_cart_total(self):
        return sum(item[3] for item in self.cart)

    def checkout(self):
        if not self.cart:
            return False, "Cart is empty"
        
        total = self.get_cart_total()
        for item in self.cart:
            self.inventory.db.record_sale(item[0], 1, item[3])  # Record sale and reduce quantity
        self.cart.clear()
        return True, f"Checkout successful. Total: ₱{total:.2f}"

    def clear_cart(self):
        self.cart.clear()

    def get_cart_items(self):
        return self.cart  # Return cart for display purposes