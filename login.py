import tkinter as tk
from tkinter import messagebox
import mongo

class LoginWindow:
    def __init__(self, parent, on_success=None):
        self.win = tk.Toplevel(parent)
        self.win.title("Vroomify Auth Gate")
        self.win.geometry("350x520")
        self.win.configure(bg="#1A110B")
        self.on_success = on_success

        # Center the window
        self.win.transient(parent)
        self.win.grab_set()

        tk.Label(self.win, text="login/signup ", fg="#D4AF37", bg="#1A110B", font=("Times New Roman", 18, "bold")).pack(pady=30)
        
        tk.Label(self.win, text="Username", bg="#1A110B", fg="#F5F5DC").pack()
        self.u = tk.Entry(self.win, width=28, font=("Arial", 11)); self.u.pack(pady=5)

        tk.Label(self.win, text="Password", bg="#1A110B", fg="#F5F5DC").pack()
        self.p = tk.Entry(self.win, show="*", width=28, font=("Arial", 11)); self.p.pack(pady=5)

        # SHOW PASSWORD TOGGLE
        self.show_p = tk.BooleanVar()
        tk.Checkbutton(self.win, text="View Password", variable=self.show_p, bg="#1A110B", 
                       fg="#D4AF37", selectcolor="#1A110B", activebackground="#1A110B", 
                       command=self.toggle_pass).pack(pady=5)

        tk.Label(self.win, text="Identify Role", bg="#1A110B", fg="#F5F5DC").pack(pady=5)
        self.role = tk.StringVar(value="Lawyer")
        self.role_menu = tk.OptionMenu(self.win, self.role, "Client", "Chief Judge", "Lawyer", "Admin")
        self.role_menu.config(bg="#D4AF37", fg="#1A110B", font=("Arial", 9, "bold"))
        self.role_menu.pack(pady=10)

        tk.Button(self.win, text="SAVE", bg="#D4AF37", fg="#1A110B", font=("Arial", 10, "bold"),
                  command=self.auth, width=20, height=2, cursor="hand2").pack(pady=20)

    def toggle_pass(self):
        self.p.config(show="" if self.show_p.get() else "*")

    def auth(self):
        username = self.u.get()
        password = self.p.get()
        role = self.role.get()

        user_data, status = mongo.smart_auth(username, password, role)

        if status == "WRONG_PASS":
            messagebox.showerror("Denied", "Incorrect Credentials. Please try again.")
        else:
            # We must destroy this window BEFORE opening the next one to avoid blank screens
            self.win.destroy()
            
            if self.on_success:
                self.on_success()
            elif role in ["Chief Judge", "Lawyer", "Admin"]:
                # Delayed import to prevent circular issues
                from admin import AdminDashboard
                AdminDashboard(user_data)