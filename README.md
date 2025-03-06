# Sari-Sari Store Inventory System

A complete inventory management system for small retail stores (Sari-Sari stores) built with Python, Tkinter GUI, and SQLite. This system provides tools for inventory tracking, point of sale operations, sales reporting, advanced analytics, and supply chain management.

## Features

### Inventory Management
- Add, update, and delete products
- Barcode/QR code support
- Supplier linking for products
- Real-time inventory updates

### Point of Sale (POS)
- Barcode/QR scanning for quick sales
- Cart management with total calculation
- Checkout processing with automatic inventory adjustment

### Reports
- Customizable sales reports by date range
- Detailed breakdown of sales by product and date

### Analytics
- **Low Stock Alerts**: Identify items with quantity ≤ 10
- **Sales Trends**: Analyze sales over the last 30 days
- **Top Products**: Rank top 5 products by sales volume
- **Sales Forecasting**:
  - Simple Moving Average (SMA)
  - Exponential Smoothing (EXP, α=0.3)
  - Linear Regression (LR)
  - 7-day forecasts based on 30-day history
- **Inventory Optimization**:
  - Economic Order Quantity (EOQ)
  - Safety Stock (2 days of average demand)
  - Reorder Point calculation

### Supply Chain Management
- Manage suppliers (add, update, delete)
- Assign suppliers to products
- Reorder recommendations based on stock levels and lead times

## File Structure

project_folder/
│
├── main.py              # Main application with GUI
├── inventory.py        # Inventory management logic
├── database.py         # SQLite database operations with schema migration
├── pos.py             # Point of Sale functionality
├── reports.py         # Sales reporting
├── analytics.py        # Analytics, forecasting, and optimization
├── supply_chain.py     # Supplier and supply chain management
└── inventory.db        # SQLite database (auto-created)

## Requirements
- **Python 3.x**
- **Tkinter** (included with Python)
- **SQLite3** (included with Python)
- **NumPy** (for Linear Regression forecasting)
  - Install with: `pip install numpy`

## Installation
1. Clone or download this repository:

   git clone [[https://github.com/mrcdctr/sari-sari-store.git]

2. Navigate to the project folder:

   cd project_folder

3. Install the required dependency:

   pip install numpy

4. Run the application:

   python main.py

## Usage
1. Launch the application with `python main.py`.
2. Use the tabbed interface to access features:
- **Inventory**: Manage products and view stock
- **Point of Sale**: Process sales transactions
- **Reports**: Generate sales reports
- **Analytics**: Analyze trends, forecast sales, and optimize inventory
- **Supply Chain**: Manage suppliers and reorder recommendations

### Inventory Management
- Add products with name, quantity, price, barcode, and optional supplier
- Update or delete products from the table
- View all products with supplier details

### Point of Sale
- Enter barcodes manually or use a scanner
- Add items to cart, view total, and checkout
- Clear cart as needed

### Reports
- Input start and end dates (YYYY-MM-DD format)
- Generate detailed sales reports

### Analytics
- **Low Stock Alert**: View items needing restock
- **Sales Trend**: See 30-day sales summary
- **Top Products**: List top 5 sellers
- **Forecast Sales**: Select a product, choose a method (SMA, EXP, LR), and view 7-day forecast
- **Optimize Inventory**: Select a product to calculate EOQ, safety stock, and reorder point

### Supply Chain
- Add suppliers with name, contact, and lead time
- Update or delete suppliers
- View reorder recommendations for selected products

## Database
- Uses SQLite (`inventory.db`) for persistent storage
- Automatically creates tables on first run
- Includes schema migration to add `supplier_id` column to existing databases
- Stores inventory, sales, and supplier data

## Notes
- **Barcode/QR Scanning**: Assumes a scanner that inputs data as keyboard input
- **Forecasting**: Requires at least 3 days of sales history
- **Optimization**: Default costs (ordering=₱50, holding=20% of unit price) can be adjusted in `analytics.py`
- **Schema Migration**: Automatically updates older databases to include `supplier_id`

## Testing
The system has been thoroughly tested:
- **Inventory**: CRUD operations, supplier linking
- **POS**: Scanning, checkout, inventory updates
- **Reports**: Date range validation, report generation
- **Analytics**: All forecasting methods (SMA, EXP, LR), optimization calculations
- **Supply Chain**: Supplier management, reorder recommendations
- **Database**: Schema creation and migration

## Troubleshooting
- **Error: "no such column: i.supplier_id"**: Fixed with schema migration in `database.py`. Run the updated code to resolve.
- **Missing NumPy**: Install with `pip install numpy`.
- **Invalid Inputs**: Error messages will guide you to correct inputs.

## Limitations
- No user authentication
- Single-user system
- Text-based analytics (no graphical charts)
- Basic barcode scanning support

## Future Enhancements
- User login system
- Graphical charts for analytics
- Multi-user support
- Receipt printing
- Advanced barcode scanner integration

## Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with your changes

## License
This project is licensed under the MIT License.

## Contact
Developed by Marco Doctor - March 2025
For issues or questions, open an issue on the repository or contact mrcdctr@gmail.com

