from database import Database


class SupplyChainManager:
    def __init__(self):
        self.db = Database()

    def add_supplier(self, name, contact, lead_time):
        try:
            lead_time = int(lead_time)
            if lead_time < 0:
                return False, "Lead time must be positive"
            self.db.add_supplier(name, contact, lead_time)
            return True, "Supplier added successfully"
        except ValueError:
            return False, "Invalid lead time format"

    def get_suppliers(self):
        return self.db.get_all_suppliers()

    def update_supplier(self, supplier_id, name, contact, lead_time):
        try:
            lead_time = int(lead_time)
            if lead_time < 0:
                return False, "Lead time must be positive"
            self.db.update_supplier(supplier_id, name, contact, lead_time)
            return True, "Supplier updated successfully"
        except ValueError:
            return False, "Invalid lead time format"

    def delete_supplier(self, supplier_id):
        self.db.delete_supplier(supplier_id)
        return True, "Supplier deleted successfully"

    def get_reorder_recommendation(self, product):
        if not product[5]:
            return "No supplier assigned"

        supplier = next((s for s in self.db.get_all_suppliers() if s[0] == product[5]), None)
        if not supplier:
            return "Supplier not found"

        return (f"Reorder Recommendation for {product[1]}\n"
                f"Current Quantity: {product[2]}\n"
                f"Supplier: {supplier[1]}\n"
                f"Contact: {supplier[2]}\n"
                f"Lead Time: {supplier[3]} days\n"
                f"Recommended Action: Order now if quantity < 10")