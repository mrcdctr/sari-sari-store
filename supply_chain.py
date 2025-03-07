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
        except Exception as e:
            return False, f"Error adding supplier: {str(e)}"

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
        except Exception as e:
            return False, f"Error updating supplier: {str(e)}"

    def delete_supplier(self, supplier_id):
        try:
            self.db.delete_supplier(supplier_id)
            return True, "Supplier deleted successfully"
        except Exception as e:
            return False, f"Error deleting supplier: {str(e)}"

    def get_reorder_recommendation(self, product):
        product_id, name, quantity, price, _, supplier_id, supplier_name = product
        sales_history = self.db.get_sales_history(product_id, 30)
        if not sales_history:
            return f"No sales data for {name} to recommend reorder"
        
        daily_avg = sum(qty for _, qty in sales_history) / len(sales_history)
        lead_time = self.db.cursor.execute('SELECT lead_time FROM suppliers WHERE id=?', 
                                          (supplier_id,)).fetchone()[0] if supplier_id else 0
        reorder_point = daily_avg * lead_time
        recommendation = f"Reorder Recommendation for {name}\n"
        recommendation += "-------------------------------------\n"
        recommendation += f"Current Stock: {quantity}\n"
        recommendation += f"Daily Avg Sales: {daily_avg:.2f}\n"
        recommendation += f"Lead Time: {lead_time} days\n"
        recommendation += f"Reorder Point: {reorder_point:.2f}\n"
        recommendation += f"Supplier: {supplier_name if supplier_name else 'None'}\n"
        recommendation += "Status: " + ("Order now" if quantity <= reorder_point else "Sufficient stock")
        return recommendation