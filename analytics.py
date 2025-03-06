from database import Database
from datetime import datetime, timedelta
import numpy as np


class InventoryAnalytics:
    def __init__(self):
        self.db = Database()

    def get_low_stock_alert(self, threshold=10):
        low_stock = self.db.get_low_stock_products(threshold)
        report = "Low Stock Alert\n"
        report += "----------------\n"
        for product in low_stock:
            report += f"ID: {product[0]}\n"
            report += f"Product: {product[1]}\n"
            report += f"Quantity: {product[2]}\n"
            report += f"Price: ₱{product[3]:.2f}\n\n"
        return report if low_stock else "No low stock items"

    def get_sales_trend_analysis(self, days=30):
        trends = self.db.get_sales_trend(days)
        report = f"Sales Trend (Last {days} Days)\n"
        report += "-------------------------\n"
        total_quantity = 0
        total_amount = 0

        for date, qty, total in trends:
            report += f"Date: {date}\n"
            report += f"Items Sold: {qty}\n"
            report += f"Total: ₱{total:.2f}\n\n"
            total_quantity += qty
            total_amount += total

        report += "-------------------------\n"
        report += f"Total Items Sold: {total_quantity}\n"
        report += f"Total Amount: ₱{total_amount:.2f}"
        return report

    def get_product_performance(self, limit=5):
        top_products = self.db.get_top_products(limit)
        report = f"Top {limit} Products\n"
        report += "-------------------\n"
        for name, qty, total in top_products:
            report += f"Product: {name}\n"
            report += f"Units Sold: {qty}\n"
            report += f"Total Sales: ₱{total:.2f}\n\n"
        return report

    def forecast_sales(self, product_id, days=30, forecast_period=7, method="sma"):
        try:
            history = self.db.get_sales_history(product_id, days)
            if not history or len(history) < 3:
                return "Insufficient data for forecasting (need at least 3 days)"

            dates, quantities = zip(*history)
            forecast = []

            if method == "sma":
                sma = sum(quantities[-3:]) / 3
                forecast = [sma] * forecast_period
            elif method == "exp":
                alpha = 0.3
                forecast = [float(quantities[-1])]
                for _ in range(forecast_period - 1):
                    forecast.append(alpha * float(quantities[-1]) + (1 - alpha) * forecast[-1])
            elif method == "lr":
                x = np.arange(len(quantities))
                y = np.array(quantities, dtype=float)
                slope, intercept = np.polyfit(x, y, 1)
                forecast = [slope * (len(quantities) + i) + intercept for i in range(forecast_period)]
            else:
                return "Invalid forecasting method"

            report = f"Sales Forecast for Next {forecast_period} Days\n"
            report += f"Method: {method.upper()}\n"
            report += "-------------------------------------\n"
            report += f"Based on {days}-day history\n"
            for i, qty in enumerate(forecast, 1):
                date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
                report += f"{date}: {qty:.2f} units\n"
            report += f"Predicted total: {sum(forecast):.2f} units"
            return report
        except Exception as e:
            return f"Error in forecasting: {str(e)}"

    def optimize_inventory(self, product_id, annual_demand=None, ordering_cost=50, holding_cost_percent=0.2):
        try:
            product = self.db.cursor.execute('SELECT * FROM inventory WHERE id=?', (product_id,)).fetchone()
            if not product:
                return "Product not found"

            if annual_demand is None:
                history = self.db.get_sales_history(product_id, 30)
                if not history or len(history) < 3:
                    return "Insufficient sales data for optimization"
                daily_avg = sum(qty for _, qty in history) / len(history)
                annual_demand = daily_avg * 365

            holding_cost = product[3] * holding_cost_percent
            eoq = ((2 * annual_demand * ordering_cost) / holding_cost) ** 0.5

            safety_stock = (annual_demand / 365) * 2
            supplier_id = product[5]
            lead_time = self.db.cursor.execute('SELECT lead_time FROM suppliers WHERE id=?',
                                               (supplier_id,)).fetchone()[0] if supplier_id else 0
            reorder_point = (annual_demand / 365) * lead_time + safety_stock

            report = f"Inventory Optimization for {product[1]}\n"
            report += "-------------------------------------\n"
            report += f"Annual Demand: {annual_demand:.2f} units\n"
            report += f"Ordering Cost: ₱{ordering_cost:.2f}\n"
            report += f"Holding Cost: ₱{holding_cost:.2f}/unit/year\n"
            report += f"Economic Order Quantity (EOQ): {eoq:.2f} units\n"
            report += f"Safety Stock: {safety_stock:.2f} units\n"
            report += f"Reorder Point: {reorder_point:.2f} units\n"
            report += f"Current Stock: {product[2]} units\n"
            report += "Recommendation: " + ("Order now" if product[2] <= reorder_point else "Sufficient stock")
            return report
        except Exception as e:
            return f"Error in optimization: {str(e)}"