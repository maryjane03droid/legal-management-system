import tkinter as tk
from tkinter import messagebox
import mongo

class SignupWindow:
    def __init__(self, root):
        self.win = tk.Toplevel(root)
        self.win.title("Create Legal Account")
        self.win.geometry("350x500")
        self.win.configure(bg="#3d2b1f") # Matching your aesthetic

        # Header
        tk.Label(self.win, text="REGISTRATION", font=("Times New Roman", 20, "bold"), 
                 bg="#3d2b1f", fg="#d4af37").pack(pady=30)

        # Username
        tk.Label(self.win, text=" Username", bg="#3d2b1f", fg="#f5f5dc").pack()
        self.u_ent = tk.Entry(self.win, font=("Arial", 11), bg="#f5f5dc")
        self.u_ent.pack(pady=5)

        # Password
        tk.Label(self.win, text="Password", bg="#3d2b1f", fg="#f5f5dc").pack()
        self.p_ent = tk.Entry(self.win, show="*", font=("Arial", 11), bg="#f5f5dc")
        self.p_ent.pack(pady=5)

        # Role Selection
        tk.Label(self.win, text="Account Type", bg="#3d2b1f", fg="#f5f5dc").pack(pady=10)
        self.role_var = tk.StringVar(value="Client")
        self.role_menu = tk.OptionMenu(self.win, self.role_var, "Client", "Judge", "Lawyer")
        self.role_menu.config(bg="#d4af37", fg="#3d2b1f")
        self.role_menu.pack()

        # Signup Button
        tk.Button(self.win, text="CREATE ACCOUNT", bg="#d4af37", fg="#3d2b1f", 
                  font=("Arial", 10, "bold"), width=20, height=2, 
                  command=self.process_signup).pack(pady=30)

    def process_signup(self):
        username = self.u_ent.get().strip()
        password = self.p_ent.get().strip()
        role = self.role_var.get()

        if not username or not password:
            messagebox.showwarning("Incomplete", "Please fill in all fields.")
            return

        # Use the smart_auth logic from mongo.py
        user, status = mongo.smart_auth(username, password, role)

        if status == "CREATED":
            messagebox.showinfo("Success", f"Account created successfully as {role}!")
            self.win.destroy()
        elif status == "SUCCESS":
            messagebox.showerror("Error", "Username already exists. Please choose another or login.")
        else:
            messagebox.showerror("Error", "Registration failed.")

# To test this file standalone:
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw() # Hide the tiny main root window
    SignupWindow(root)
    root.mainloop()