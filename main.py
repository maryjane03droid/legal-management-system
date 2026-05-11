import tkinter as tk
from tkinter import ttk, messagebox
from database_manager import DatabaseManager

class LegalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Legal Management System")
        self.root.geometry("800x600")
        
        # This connects to your database_manager.py file
        self.db = DatabaseManager()
        
        self.create_widgets()

    def create_widgets(self):
        # 1. Title
        tk.Label(self.root, text="Law Firm Dashboard", font=("Arial", 20, "bold")).pack(pady=20)
        
        # 2. Registration Form
        form_frame = tk.LabelFrame(self.root, text="Client Intake", padx=10, pady=10)
        form_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(form_frame, text="Full Name:").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Phone:").grid(row=1, column=0, sticky="w")
        self.phone_entry = tk.Entry(form_frame)
        self.phone_entry.grid(row=1, column=1, pady=5, padx=5)

        # 3. Save Button
        save_btn = tk.Button(self.root, text="Add to Database", bg="green", fg="white", command=self.save_client)
        save_btn.pack(pady=10)

        # 4. The Table
        self.tree = ttk.Treeview(self.root, columns=("Name", "Phone"), show='headings')
        self.tree.heading("Name", text="Client Name")
        self.tree.heading("Phone", text="Phone Number")
        self.tree.pack(pady=20, fill="both", expand=True, padx=20)
        
        self.refresh_table()

    def save_client(self):
        """This is the function the error was missing"""
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        if name and phone:
            self.db.add_client(name, phone, "legal@example.com")
            messagebox.showinfo("Success", f"Client {name} added!")
            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.refresh_table()
        else:
            messagebox.showwarning("Warning", "Fields cannot be empty!")

    def refresh_table(self):
        """Clears and reloads the list from MongoDB"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        clients = self.db.get_all_clients()
        for client in clients:
            self.tree.insert("", tk.END, values=(client['name'], client['phone']))

if __name__ == "__main__":
    root = tk.Tk()
    app = LegalApp(root)
    # This keeps the window open
    root.mainloop()