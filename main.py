import tkinter as tk
from tkinter import ttk, messagebox
from database_manager import DatabaseManager

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Legal System - Staff Login")
        self.root.geometry("350x300")
        self.root.configure(bg="#3d2b1f") 
        self.db = DatabaseManager()

        tk.Label(root, text="Staff Authentication", font=("Times New Roman", 18, "bold"), 
                 bg="#3d2b1f", fg="#d4af37").pack(pady=20)

        tk.Label(root, text="Username:", bg="#3d2b1f", fg="#f5f5dc").pack()
        self.username_entry = tk.Entry(root, bg="#f5f5dc")
        self.username_entry.pack(pady=5)

        tk.Label(root, text="Password:", bg="#3d2b1f", fg="#f5f5dc").pack()
        self.password_entry = tk.Entry(root, show="*", bg="#f5f5dc")
        self.password_entry.pack(pady=5)

        tk.Button(root, text="Secure Login", bg="#d4af37", fg="#3d2b1f", 
                  font=("Arial", 10, "bold"), command=self.handle_login).pack(pady=20)

    def handle_login(self):
        user = self.username_entry.get()
        pw = self.password_entry.get()
        if self.db.check_login(user, pw):
            self.root.destroy() 
            launch_dashboard()
        else:
            messagebox.showerror("Access Denied", "Invalid Credentials")

class LegalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Legal Management System")
        self.root.geometry("900x700")

        self.bg_color = "#3d2b1f"  # Deep Brown
        self.fg_color = "#f5f5dc"  # Beige
        self.gold_accent = "#d4af37" # Gold
        
        self.db = DatabaseManager()
        self.create_widgets()

    def create_widgets(self):
        self.root.configure(bg=self.bg_color)
        
        tk.Label(self.root, text="Law Firm Dashboard",
                 font=("Times New Roman", 28, "bold"),
                 bg=self.bg_color, fg=self.gold_accent).pack(pady=20)

        # Registration Form
        form_frame = tk.LabelFrame(self.root, text="Client Intake",
                                   bg=self.bg_color, fg=self.gold_accent,
                                   font=("arial", 10 ,"bold"), padx=20, pady=10)
        form_frame.pack(pady=10, padx=20, fill="x")
    
        tk.Label(form_frame, text="Full Name:", bg=self.bg_color, fg=self.fg_color).grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(form_frame, bg=self.fg_color)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Phone:", bg=self.bg_color, fg=self.fg_color).grid(row=1, column=0, sticky="w")
        self.phone_entry = tk.Entry(form_frame, bg=self.fg_color)
        self.phone_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Case Type:", bg=self.bg_color, fg=self.fg_color).grid(row=2, column=0, sticky="w")
        self.case_type_var = tk.StringVar()
        self.case_dropdown = ttk.Combobox(form_frame, textvariable=self.case_type_var, state="readonly")
        self.case_dropdown['values'] = ("Family Law", "Criminal Defense", "Corporate", "Estate Planning")
        self.case_dropdown.grid(row=2, column=1, pady=5, padx=5)
        self.case_dropdown.current(0)

        # Buttons
        save_btn = tk.Button(self.root, text="Add to Database", bg=self.gold_accent, 
                             fg=self.bg_color, font=("Arial", 10, "bold"), command=self.save_client)
        save_btn.pack(pady=10)

        delete_btn = tk.Button(self.root, text="Delete Selected Client", bg="#8b0000", 
                               fg="white", font=("Arial", 10, "bold"), command=self.delete_selected)
        delete_btn.pack(pady=5)

        # Table Styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=self.fg_color, foreground=self.bg_color, 
                        fieldbackground=self.fg_color, rowheight=30)
        style.configure("Treeview.Heading", background=self.gold_accent, foreground=self.bg_color, font=("Arial", 10, "bold"))
        style.map("Treeview", background=[('selected', self.gold_accent)])

        self.tree = ttk.Treeview(self.root, columns=("Name", "Phone", "Type"), show='headings')
        self.tree.heading("Name", text="Client Name")
        self.tree.heading("Phone", text="Phone Number")
        self.tree.heading("Type", text="Case Category")
        self.tree.pack(pady=20, fill="both", expand=True, padx=20)
        
        self.refresh_table()

    def save_client(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        case_type = self.case_type_var.get()
        if name and phone:
            self.db.add_client(name, phone, "legal@example.com", case_type)
            messagebox.showinfo("Success", f"Client {name} added!")
            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.refresh_table()
        else:
            messagebox.showwarning("Warning", "Fields cannot be empty!")

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for client in self.db.get_all_clients():
            self.tree.insert("", tk.END, iid=str(client['_id']), 
                             values=(client['name'], client['phone'], client.get('case_type', 'General')))

    def delete_selected(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Select a client to delete.")
            return

        if messagebox.askyesno("Confirm Delete", "Permanently delete this client?"):
            self.db.delete_client(selected_item[0])
            self.refresh_table()
            messagebox.showinfo("Success", "Client record deleted.")

# --- LAUNCH LOGIC (Must be outside the classes) ---
def launch_dashboard():
    dashboard_root = tk.Tk()
    app = LegalApp(dashboard_root)
    dashboard_root.mainloop()
    
if __name__ == "__main__":
    login_root = tk.Tk()
    LoginWindow(login_root)
    login_root.mainloop()