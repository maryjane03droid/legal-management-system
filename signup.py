import tkinter as tk
from tkinter import messagebox, ttk
import mongo
from login import LoginWindow # Import LoginWindow to allow jumping back

class SignupWindow:
    def __init__(self, parent, is_admin=False):
        self.win = tk.Toplevel(parent)
        self.win.title("PRESTIGE REGISTRATION")
        self.win.geometry("400x650") # Slightly taller to fit the new button
        self.win.configure(bg="#1A110B")
        self.is_admin = is_admin
        self.is_shon = False
        
        title_text = "STAFF REGISTRATION" if is_admin else "CLIENT REGISTRATION"
        tk.Label(self.win, text=title_text, font=("Times New Roman", 16, "bold"), 
                 bg="#1A110B", fg="#D4AF37").pack(pady=(30, 20))
        
        f = tk.Frame(self.win, bg="#1A110B")
        f.pack(padx=40, fill="x")

        # --- USERNAME ---
        tk.Label(f, text="Choose Username", bg="#1A110B", fg="#A89276", font=("Arial", 9)).pack(anchor="w")
        self.u = tk.Entry(f, bg="#2C1E16", fg="white", borderwidth=0, insertbackground="#D4AF37")
        self.u.pack(fill="x", pady=(5, 15), ipady=5)
        
        # --- PASSWORD WITH VIEW TOGGLE ---
        tk.Label(f, text="Choose Password", bg="#1A110B", fg="#A89276", font=("Arial", 9)).pack(anchor="w")
        pass_row = tk.Frame(f, bg="#2C1E16")
        pass_row.pack(fill="x", pady=(5, 15))
        
        self.p = tk.Entry(pass_row, show="*", bg="#2C1E16", fg="white", borderwidth=0, insertbackground="#D4AF37")
        self.p.pack(side="left", fill="x", expand=True, ipady=5, padx=5)
        
        self.toggle_btn = tk.Button(pass_row, text="👁", bg="#2C1E16", fg="#D4AF37", borderwidth=0, 
                                    activebackground="#2C1E16", cursor="hand2", command=self.toggle_pass)
        self.toggle_btn.pack(side="right", padx=5)

        # --- ADMIN ONLY FIELDS ---
        if self.is_admin:
            tk.Label(f, text="Staff Security Code", bg="#1A110B", fg="#D4AF37", font=("Arial", 9, "bold")).pack(anchor="w")
            self.secret_ent = tk.Entry(f, show="*", bg="#2C1E16", fg="white", borderwidth=0, insertbackground="#D4AF37")
            self.secret_ent.pack(fill="x", pady=(5, 15), ipady=5)

            tk.Label(f, text="Professional Role", bg="#1A110B", fg="#A89276", font=("Arial", 9)).pack(anchor="w")
            self.r = ttk.Combobox(f, values=["Lawyer", "Judge"], state="readonly")
            self.r.current(0)
            self.r.pack(fill="x", pady=(5, 20))
        
        # --- ACTION BUTTONS ---
        tk.Button(self.win, text="CREATE ACCOUNT", bg="#D4AF37", fg="black", font=("Arial", 10, "bold"),
                  height=2, width=22, bd=0, cursor="hand2", command=self.save).pack(pady=(20, 10))

        # NEW: Login Link for existing users
        tk.Button(self.win, text="Already have an account? Log In", bg="#1A110B", fg="#A89276", 
                  font=("Arial", 9, "underline"), bd=0, cursor="hand2", 
                  activebackground="#1A110B", activeforeground="#D4AF37",
                  command=self.switch_to_login).pack()

    def toggle_pass(self):
        """Toggle password visibility"""
        if self.is_shon:
            self.p.config(show="*")
            self.toggle_btn.config(fg="#D4AF37")
            self.is_shon = False
        else:
            self.p.config(show="")
            self.toggle_btn.config(fg="white")
            self.is_shon = True

    def switch_to_login(self):
        """Closes signup and opens login directly"""
        parent = self.win.master
        # Access the login_success callback from the parent app if possible
        # In your main.py setup, LegalFirmPortal is the master
        self.win.destroy()
        LoginWindow(parent, on_success=lambda user: parent.nametowidget('.').app.login_success(user) if hasattr(parent, 'app') else None)
        # Note: If using the provided main.py, the standard trigger is:
        # LoginWindow(parent, on_success=self.parent_app.login_success)

    def save(self):
        username, password = self.u.get(), self.p.get()
        if not username or not password:
            messagebox.showwarning("Incomplete", "Please fill in all fields.")
            return

        if self.is_admin:
            if self.secret_ent.get() != "ce02b":
                messagebox.showerror("Security Alert", "Invalid Staff Code.")
                return
            role = self.r.get()
        else:
            role = "Client"

        if mongo.create_user(username, password, role):
            messagebox.showinfo("Success", f"Account created as {role}. Please log in.")
            self.win.destroy()
        else:
            
            messagebox.showerror("Error", "Username is already registered.")