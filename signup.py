import tkinter as tk
from tkinter import messagebox
import mongo # Ensure mongo.py is in the same folder

class SignupWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Staff Registration - Legal System")
        self.root.geometry("400x450")
        self.root.configure(bg="#3d2b1f") # Deep Brown

        # Header
        tk.Label(self.root, text="Create Staff Account", font=("Times New Roman", 20, "bold"), 
                 bg="#3d2b1f", fg="#d4af37").pack(pady=30)

        # Username
        tk.Label(self.root, text="Desired Username:", bg="#3d2b1f", fg="#f5f5dc").pack()
        self.user_entry = tk.Entry(self.root, bg="#f5f5dc", width=30)
        self.user_entry.pack(pady=10)

        # Password
        tk.Label(self.root, text="Secure Password:", bg="#3d2b1f", fg="#f5f5dc").pack()
        self.pw_entry = tk.Entry(self.root, show="*", bg="#f5f5dc", width=30)
        self.pw_entry.pack(pady=10)

        # Signup Button
        tk.Button(self.root, text="Register Staff", bg="#d4af37", fg="#3d2b1f", 
                  font=("Arial", 11, "bold"), width=20, command=self.register).pack(pady=30)

        self.root.mainloop()

    def register(self):
        username = self.user_entry.get()
        password = self.pw_entry.get()

        if username and password:
            # Calls the signup_staff function in your mongo.py
            success = mongo.signup_staff(username, password)
            if success:
                messagebox.showinfo("Success", "Account created! You can now log in.")
                self.root.destroy()
            else:
                messagebox.showerror("Error", "Username already exists in the system.")
        else:
            messagebox.showwarning("Incomplete", "Please fill in all fields.")

if __name__ == "__main__":
    SignupWindow()