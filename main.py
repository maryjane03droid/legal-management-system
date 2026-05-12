import tkinter as tk
from tkinter import ttk, messagebox
import mongo # Imports your updated mongo.py

class AuthPopup:
    def __init__(self, parent, action_to_perform):
        self.popup = tk.Toplevel(parent)
        self.popup.title("Staff Access")
        self.popup.geometry("350x350")
        self.popup.configure(bg="#3d2b1f")
        self.action_to_perform = action_to_perform

        tk.Label(self.popup, text="Security Gate", font=("Times New Roman", 18, "bold"), 
                 bg="#3d2b1f", fg="#d4af37").pack(pady=15)

        tk.Label(self.popup, text="Username:", bg="#3d2b1f", fg="#f5f5dc").pack()
        self.user_entry = tk.Entry(self.popup, bg="#f5f5dc")
        self.user_entry.pack(pady=5)

        tk.Label(self.popup, text="Password:", bg="#3d2b1f", fg="#f5f5dc").pack()
        self.pw_entry = tk.Entry(self.popup, show="*", bg="#f5f5dc")
        self.pw_entry.pack(pady=5)

        # Login Button
        tk.Button(self.popup, text="Login & Proceed", bg="#d4af37", fg="#3d2b1f", 
                  font=("Arial", 10, "bold"), width=20, command=self.handle_login).pack(pady=10)

        # Signup Button (To create the accounts that aren't working)
        tk.Button(self.popup, text="Signup New Staff", bg="#5c4033", fg="#f5f5dc", 
                  font=("Arial", 9), width=20, command=self.handle_signup).pack()

    def handle_login(self):
        if mongo.check_login(self.user_entry.get(), self.pw_entry.get()):
            self.popup.destroy()
            self.action_to_perform()
        else:
            messagebox.showerror("Error", "Invalid Credentials")

    def handle_signup(self):
        user = self.user_entry.get()
        pw = self.pw_entry.get()
        if user and pw:
            if mongo.signup_staff(user, pw):
                messagebox.showinfo("Success", "Staff account created! You can now login.")
            else:
                messagebox.showerror("Error", "Username already exists.")
        else:
            messagebox.showwarning("Warning", "Fields cannot be empty.")

class LegalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Legal Management System")
        self.root.geometry("900x700")
        self.root.configure(bg="#3d2b1f")
        
        self.db = mongo 
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Law Firm Dashboard", font=("Times New Roman", 28, "bold"),
                 bg="#3d2b1f", fg="#d4af37").pack(pady=20)

        # Entry Form
        form = tk.LabelFrame(self.root, text="Case Entry", bg="#3d2b1f", fg="#d4af37", padx=20, pady=10)
        form.pack(pady=10, padx=20, fill="x")
    
        tk.Label(form, text="Client Name:", bg="#3d2b1f", fg="#f5f5dc").grid(row=0, column=0, sticky="w")
        self.name_in = tk.Entry(form, bg="#f5f5dc")
        self.name_in.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(form, text="Phone:", bg="#3d2b1f", fg="#f5f5dc").grid(row=1, column=0, sticky="w")
        self.phone_in = tk.Entry(form, bg="#f5f5dc")
        self.phone_in.grid(row=1, column=1, pady=5, padx=5)

        # Trigger Auth Pop-up on "Add Case"
        tk.Button(self.root, text="Add Case", bg="#d4af37", fg="#3d2b1f", font=("Arial", 10, "bold"),
                  command=lambda: AuthPopup(self.root, self.save_data)).pack(pady=10)

        # Table
        self.tree = ttk.Treeview(self.root, columns=("N", "P", "S"), show='headings')
        self.tree.heading("N", text="Client Name")
        self.tree.heading("P", text="Phone")
        self.tree.heading("S", text="Status")
        self.tree.pack(pady=20, fill="both", expand=True, padx=20)
        self.refresh()

    def save_data(self):
        name = self.name_in.get()
        phone = self.phone_in.get()
        if name and phone:
            self.db.add_new_case(name, phone, "General") # Saves to MongoDB
            messagebox.showinfo("Success", "Data saved to MongoDB Atlas.")
            self.refresh()
        else:
            messagebox.showwarning("Empty Fields", "Please enter details.")

    def refresh(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for case in self.db.get_all_cases():
            self.tree.insert("", "end", values=(case['client_name'], case['phone'], case['status']))

if __name__ == "__main__":
    root = tk.Tk()
    LegalApp(root)
    root.mainloop()