import tkinter as tk
from tkinter import messagebox
import mongo 
import main # Import your main.py to launch the dashboard

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Staff Login - Legal System")
        self.root.geometry("400x450")
        self.root.configure(bg="#3d2b1f")

        # Header
        tk.Label(self.root, text="Legal System Login", font=("Times New Roman", 22, "bold"), 
                 bg="#3d2b1f", fg="#d4af37").pack(pady=40)

        # Credentials
        tk.Label(self.root, text="Username", bg="#3d2b1f", fg="#f5f5dc").pack()
        self.user_entry = tk.Entry(self.root, bg="#f5f5dc", width=30)
        self.user_entry.pack(pady=10)

        tk.Label(self.root, text="Password", bg="#3d2b1f", fg="#f5f5dc").pack()
        self.pw_entry = tk.Entry(self.root, show="*", bg="#f5f5dc", width=30)
        self.pw_entry.pack(pady=10)

        # Login Button
        tk.Button(self.root, text="Authenticate", bg="#d4af37", fg="#3d2b1f", 
                  font=("Arial", 11, "bold"), width=20, command=self.login).pack(pady=30)

        self.root.mainloop()

    def login(self):
        username = self.user_entry.get()
        password = self.pw_entry.get()

        # Checks MongoDB via mongo.py
        if mongo.check_login(username, password):
            messagebox.showinfo("Access Granted", f"Welcome, {username}")
            self.root.destroy()
            self.open_dashboard()
        else:
            messagebox.showerror("Access Denied", "Invalid Username or Password.")

    def open_dashboard(self):
        # Launches the LegalApp from your main.py
        dashboard_root = tk.Tk()
        main.LegalApp(dashboard_root)
        dashboard_root.mainloop()

if __name__ == "__main__":
    LoginWindow()