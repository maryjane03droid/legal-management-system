import tkinter as tk
from tkinter import messagebox
import mongo

class LoginWindow:
    def __init__(self, parent, on_success):
        self.win = tk.Toplevel(parent)
        self.win.title("SECURE ACCESS")
        self.win.geometry("400x550")
        self.win.configure(bg="#1A110B")
        self.on_success = on_success
        self.is_shon = False

        # --- REFINED LOGO/HEADER ---
        tk.Label(self.win, text="V A U L T  A C C E S S", font=("Times New Roman", 20, "bold"), 
                 bg="#1A110B", fg="#D4AF37").pack(pady=(50, 30))
        
        f = tk.Frame(self.win, bg="#1A110B")
        f.pack(padx=45, fill="x")

        # --- USERNAME FIELD ---
        tk.Label(f, text="Username", bg="#1A110B", fg="#A89276", font=("Arial", 9, "bold")).pack(anchor="w")
        self.u = tk.Entry(f, bg="#2C1E16", fg="white", borderwidth=0, 
                          font=("Arial", 11), insertbackground="#D4AF37")
        self.u.pack(fill="x", pady=(5, 20), ipady=8)

        # --- PASSWORD FIELD ---
        tk.Label(f, text="Password", bg="#1A110B", fg="#A89276", font=("Arial", 9, "bold")).pack(anchor="w")
        
        pass_row = tk.Frame(f, bg="#2C1E16")
        pass_row.pack(fill="x", pady=(5, 10))
        
        self.p = tk.Entry(pass_row, show="*", bg="#2C1E16", fg="white", borderwidth=0, 
                          font=("Arial", 11), insertbackground="#D4AF37")
        self.p.pack(side="left", fill="x", expand=True, ipady=8, padx=5)
        
        # Visibility Toggle
        self.toggle_btn = tk.Button(pass_row, text="👁", bg="#2C1E16", fg="#D4AF37", borderwidth=0, 
                                    activebackground="#2C1E16", activeforeground="white",
                                    cursor="hand2", command=self.toggle_pass)
        self.toggle_btn.pack(side="right", padx=5)

        # --- LOGIN ACTION ---
        tk.Button(self.win, text="AUTHORIZE", bg="#D4AF37", fg="black", font=("Arial", 10, "bold"),
                  height=2, width=22, bd=0, cursor="hand2", 
                  command=self.attempt).pack(pady=40)
        
        # Footer decoration
        tk.Label(self.win, text="PRESTIGE LEGAL SYSTEMS © 2026", font=("Arial", 7), 
                 bg="#1A110B", fg="#4A3728").pack(side="bottom", pady=10)

    def toggle_pass(self):
        """Switches password visibility with UI feedback."""
        if self.is_shon:
            self.p.config(show="*")
            self.toggle_btn.config(fg="#D4AF37")
            self.is_shon = False
        else:
            self.p.config(show="")
            self.toggle_btn.config(fg="white")
            self.is_shon = True

    def attempt(self):
        """Verifies credentials against the Cloud Atlas database."""
        username = self.u.get().strip()
        password = self.p.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Incomplete", "Access denied. Please provide all credentials.")
            return

        # Call the upgraded mongo verify function
        user = mongo.verify_user(username, password)
        
        if user:
            messagebox.showinfo("Identity Verified", f"Welcome back, {user['role']} {user['username']}.")
            self.on_success(user)
            self.win.destroy()
        else:
            messagebox.showerror("Auth Error", "The credentials provided do not match our records.")