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

if __name__ == "__main__":
    window = tk.Tk()
    app = LegalApp(window)
    window.mainloop()