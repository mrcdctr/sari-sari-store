import tkinter as tk
from tkinter import ttk, messagebox
import bcrypt
from database import Database
import sqlite3

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.root.title("Login - Sari-Sari Store")
        self.root.geometry("300x200")
        self.db = Database()
        self.on_login_success = on_login_success
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(self.root)
        self.username_entry.pack(pady=5)

        ttk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        ttk.Button(self.root, text="Login", command=self.login).pack(pady=10)
        ttk.Button(self.root, text="Register", command=self.register).pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get().encode('utf-8')
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        user = self.db.cursor.execute("SELECT id, password FROM users WHERE username=?", (username,)).fetchone()
        if user and bcrypt.checkpw(password, user[1]):
            print(f"Login successful for user_id: {user[0]}")
            try:
                for widget in self.root.winfo_children():
                    widget.destroy()
                print("Cleared login widgets, calling on_login_success")
                self.on_login_success(user[0])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start main app: {str(e)}")
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get().encode('utf-8')
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        try:
            self.db.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
            self.db.conn.commit()
            messagebox.showinfo("Success", "User registered successfully")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")