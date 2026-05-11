import tkinter as tk
from tkinter import ttk, messagebox

from database_manager import DatabaseManager

class LegalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Legal Management System")
        self.root.geometry("800x600")
        
        # Initialize our database connection
        self.db = DatabaseManager()
        
        # Create the UI layout
        self.create_widgets()

    def create_widgets(self):
        # Create a title label 
        title = tk.Label(self.root, text="Law Firm Dashboard", font=("Arial", 20, "bold"))
        title.pack(pady=20)
        
        # This is where we will add our forms and tables in the next commits
        self.status_label = tk.Label(self.root, text="System Ready", fg="green")
        self.status_label.pack(side="bottom")
        def create_widgets(self):
        # 1. Title
        tk.Label(self.root, text="Client Registration", font=("Arial", 16, "bold")).pack(pady=10)

        # 2. Input Frame
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)

        # Name Field
        tk.Label(form_frame, text="Full Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Phone Field
        tk.Label(form_frame, text="Phone Number:").grid(row=1, column=0, padx=5, pady=5)
        self.phone_entry = tk.Entry(form_frame)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)

        # Save Button
        save_btn = tk.Button(self.root, text="Add to Database", command=self.save_client)
        save_btn.pack(pady=10)
        # 3. The Table (Treeview)
        self.tree = ttk.Treeview(self.root, columns=("Name", "Phone"), show='headings')
        self.tree.heading("Name", text="Client Name")
        self.tree.heading("Phone", text="Phone Number")
        self.tree.pack(pady=20, fill="both", expand=True)
        
        # Load existing data immediately
        self.refresh_table()

def save_client(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()

        if name and phone:
            # This calls the 'add_client' function in your database_manager.py
            self.db.add_client(name, phone, "legal@example.com") 
            messagebox.showinfo("Success", f"Recorded {name} in the system!")
            
            # Clear the boxes and refresh the list
            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.refresh_table()
        else:
            messagebox.showwarning("Error", "All fields are required!")

def refresh_table(self):
        # Clear the table first
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Get data from MongoDB 
        clients = self.db.get_all_clients()
        for client in clients:
            # Insert name and phone into the UI table
            self.tree.insert("", tk.END, values=(client['name'], client['phone']))
if __name__ == "__main__":
    window = tk.Tk()
    app = LegalApp(window)
    window.mainloop()