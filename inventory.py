from database import Database

class InventoryManager:
    def __init__(self):
        self.db = Database()

    def add_item(self, name, quantity, price, barcode, supplier_id=None):
        try:
            quantity = int(quantity)
            price = float(price)
            if quantity < 0 or price < 0:
                return False, "Quantity and price must be positive"
            self.db.add_product(name, quantity, price, barcode, supplier_id)
            return True, "Product added successfully"
        except ValueError:
            return False, "Invalid quantity or price format"
        except Exception as e:
            return False, f"Error adding product: {str(e)}"

    def get_items(self):
        return self.db.get_all_products()

    def get_item_by_barcode(self, barcode):
        return self.db.get_product_by_barcode(barcode)

    def update_item(self, product_id, name, quantity, price, barcode, supplier_id=None):
        try:
            quantity = int(quantity)
            price = float(price)
            if quantity < 0 or price < 0:
                return False, "Quantity and price must be positive"
            self.db.update_product(product_id, name, quantity, price, barcode, supplier_id)
            return True, "Product updated successfully"
        except ValueError:
            return False, "Invalid quantity or price format"
        except Exception as e:
            return False, f"Error updating product: {str(e)}"

    def delete_item(self, product_id):
        try:
            self.db.delete_product(product_id)
            return True, "Product deleted successfully"
        except Exception as e:
            return False, f"Error deleting product: {str(e)}"