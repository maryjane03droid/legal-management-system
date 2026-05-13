import tkinter as tk
from tkinter import ttk, messagebox
import mongo

class AdminDashboard:
    def __init__(self, user):
        self.root = tk.Toplevel()
        self.root.title("Legal Review Board | Official Staff Portal")
        self.root.geometry("1150x750")
        self.root.configure(bg="#1A110B") 
        self.user = user

        # Force render & focus
        self.root.transient()
        self.root.grab_set()
        self.root.focus_force()

        # 1. Navbar
        nav = tk.Frame(self.root, bg="#2C1E16", height=70)
        nav.pack(fill="x", side="top")
        
        tk.Button(nav, text="← EXIT TO PORTAL", bg="#D4AF37", fg="#1A110B", 
                  font=("Arial", 9, "bold"), padx=15, command=self.root.destroy).pack(side="left", padx=20, pady=15)
        
        tk.Label(nav, text=f"OFFICIAL: {self.user['username'].upper()} ({self.user['role']})", 
                 fg="#D4AF37", bg="#2C1E16", font=("Times New Roman", 14, "bold")).pack(side="right", padx=30)

        # 2. Main Container
        main_f = tk.Frame(self.root, bg="#1A110B")
        main_f.pack(fill="both", expand=True, padx=40, pady=20)

        # Table Styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#3d2b1f", foreground="white", fieldbackground="#3d2b1f", rowheight=40, borderwidth=1)
        style.configure("Treeview.Heading", background="#2C1E16", foreground="#D4AF37", font=("Arial", 10, "bold"))

        cols = ("ID", "Client", "Case Description", "Status")
        self.tree = ttk.Treeview(main_f, columns=cols, show="headings")
        
        for col in cols:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, anchor="center", width=400 if col == "Case Description" else 150)
            
        self.tree.pack(fill="both", expand=True)
        # Bind selection event to show/hide delete button
        self.tree.bind("<<TreeviewSelect>>", self.toggle_delete_button)

        # 3. Control Panel
        self.btn_f = tk.Frame(self.root, bg="#1A110B")
        self.btn_f.pack(side="bottom", pady=40)
        
        tk.Button(self.btn_f, text="APPROVE CASE", bg="#2E7D32", fg="white", width=20, height=2, 
                  font=("Arial", 10, "bold"), command=lambda: self.review("Approved")).grid(row=0, column=0, padx=15)
        
        tk.Button(self.btn_f, text="REJECT CASE", bg="#C62828", fg="white", width=20, height=2, 
                  font=("Arial", 10, "bold"), command=lambda: self.review("Rejected")).grid(row=0, column=1, padx=15)

        # 4. Hidden Delete Button (Initialized but not packed)
        self.del_btn = tk.Button(self.btn_f, text="PERMANENT DELETE", bg="black", fg="red", width=20, height=2, 
                                 font=("Arial", 10, "bold", "underline"), command=self.drop)

        self.refresh()
        self.root.update_idletasks()

    def toggle_delete_button(self, event):
        """Shows the delete button ONLY if the selected case is Rejected."""
        selected = self.tree.selection()
        if not selected:
            return

        # Get status from the 4th column (index 3)
        item_status = self.tree.item(selected[0])['values'][3]

        if item_status == "Rejected":
            self.del_btn.grid(row=0, column=2, padx=15) # Show it
        else:
            self.del_btn.grid_forget() # Hide it

    def review(self, status):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Please select a case to review.")
            return
        
        identity = f"{self.user['username']} ({self.user['role']})"
        mongo.update_status(selected[0], status, identity)
        self.refresh()
        # Re-check visibility after refresh
        self.toggle_delete_button(None)

    def drop(self):
        selected = self.tree.selection()
        if selected and messagebox.askyesno("Final Warning", "Delete this rejected case from the system permanently?"):
            mongo.delete_case(selected[0])
            self.refresh()
            self.del_btn.grid_forget()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            data = mongo.get_cases()
            for c in data:
                self.tree.insert("", "end", iid=str(c['_id']), 
                                 values=(str(c['_id'])[-5:], c['name'], c.get('desc', 'N/A'), c['status']))
        except Exception as e:
            print(f"Sync Error: {e}")