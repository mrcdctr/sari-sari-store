Sari-Sari Store Management System

A Python-based desktop application for managing a small retail store (sari-sari store). Built with Tkinter, this system provides inventory tracking, point-of-sale (POS) functionality, sales reporting, analytics, and supply chain management.

Features
User Authentication: Secure login and registration with password hashing (bcrypt).
Inventory Management: Add, update, delete, and view product details with transaction history.
Point of Sale (POS): Scan products via barcode (manual entry or webcam), manage cart, and process checkouts.
Reports: Generate sales reports for specified date ranges.
Analytics: Monitor low stock, sales trends, top products, and forecast demand with visualization (Matplotlib).
Supply Chain: Manage suppliers and get reorder recommendations.

Requirements
Python 3.12+

Virtual environment (recommended)

Dependencies:
bcrypt

matplotlib

opencv-python

numpy

pyzbar

Setup
Clone the Repository:

git clone https://github.com/yourusername/sari-sari-store.git
cd sari-sari-store

Create and Activate a Virtual Environment:
Windows:

python -m venv .venv
.venv\Scripts\activate

Linux/macOS:

python3 -m venv .venv
source .venv/bin/activate

Install Dependencies:

pip install bcrypt matplotlib opencv-python numpy pyzbar

Run the Application:

python main.py

Usage
Login or Register:
Launch the app and register a new user (e.g., username: admin, password: password123).

Log in with your credentials.

Main Interface:
Inventory Tab: Manage products (add, update, delete) and view transaction history.

POS Tab: Scan items (type barcode or use webcam), add to cart, and checkout.

Reports Tab: Enter date range (YYYY-MM-DD) to generate sales reports.

Analytics Tab: Check stock alerts, trends, and forecasts; plot data visualizations.

Supply Chain Tab: Add/update suppliers and view reorder suggestions.

Exit: Close the window to exit the application.

Database
Uses SQLite (inventory.db) to store:
Users (username, hashed password)

Inventory (products, quantities, prices, barcodes)

Sales (transactions)

Suppliers (details)

Inventory transactions (history)

Troubleshooting
App Closes After Login: Ensure all dependencies are installed and check console output for errors.

Camera Scan Fails: Verify webcam access and opencv-python/pyzbar installation.

Errors: Run with python -m main for detailed stack traces.

Contributing
Fork the repository.

Create a feature branch (git checkout -b feature-name).

Commit changes (git commit -m "Add feature").

Push to the branch (git push origin feature-name).

Open a pull request.

License
This project is licensed under the MIT License—see LICENSE for details.

## Contact
Developed by Marco Doctor - March 2025
For issues or questions, open an issue on the repository or contact mrcdctr@gmail.com

