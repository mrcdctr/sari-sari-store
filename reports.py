from database import Database


class ReportGenerator:
    def __init__(self):
        self.db = Database()

    def generate_sales_report(self, start_date, end_date):
        sales = self.db.get_sales_report(start_date, end_date)
        report = "Sales Report\n"
        report += f"Period: {start_date} to {end_date}\n"
        report += "----------------------------------------\n"
        total_sales = 0

        for product_name, quantity, total, date in sales:
            report += f"Date: {date}\n"
            report += f"Product: {product_name}\n"
            report += f"Quantity Sold: {quantity}\n"
            report += f"Total: ₱{total:.2f}\n\n"
            total_sales += total

        report += "----------------------------------------\n"
        report += f"Grand Total: ₱{total_sales:.2f}"
        return report