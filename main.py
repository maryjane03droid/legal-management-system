import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mongo
from login import LoginWindow

class LegalManagementFirm:
    def __init__(self, root):
        self.root = root
        self.root.title("Legal Management Firm | Client Portal")
        self.root.geometry("1300x850") # Slightly wider to accommodate description
        self.root.configure(bg="#2C1E16") # Mahogany

        self.gold, self.mahogany = "#D4AF37", "#2C1E16"
        self.setup_styles()
        self.setup_ui()
        self.refresh()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Enhanced Table Styling with visible grid lines
        style.configure("Treeview", 
                        background="#3d2b1f", 
                        foreground="white", 
                        rowheight=40, 
                        fieldbackground="#3d2b1f",
                        borderwidth=1)
        
        style.map("Treeview", 
                  background=[('selected', self.gold)], 
                  foreground=[('selected', 'black')])

        # Header styling with gold borders
        style.configure("Treeview.Heading", 
                        background="#1A110B", 
                        foreground=self.gold, 
                        font=("Times New Roman", 11, "bold"),
                        borderwidth=1,
                        relief="raised")

    def setup_ui(self):
        # Premium Navbar
        nav = tk.Frame(self.root, bg="#1A110B", height=90)
        nav.pack(fill="x")
        tk.Label(nav, text="LEGAL MANAGEMENT FIRM", font=("Times New Roman", 26, "bold"), 
                 bg="#1A110B", fg=self.gold).pack(pady=20)

        # Input Card Section
        card = tk.LabelFrame(self.root, text=" CASE FILING PORTAL ", bg=self.mahogany, 
                             fg=self.gold, padx=25, pady=25, font=("Arial", 10, "bold"))
        card.pack(fill="x", padx=50, pady=20)

        # Grid Layout for Inputs
        tk.Label(card, text="Client Name:", bg=self.mahogany, fg="#F5F5DC").grid(row=0, column=0, sticky="w")
        self.n_ent = tk.Entry(card, width=25, font=("Arial", 11), bg="#3d2b1f", fg="white", insertbackground="white")
        self.n_ent.grid(row=0, column=1, padx=15)

        tk.Label(card, text="Phone Number:", bg=self.mahogany, fg="#F5F5DC").grid(row=0, column=2, sticky="w")
        self.p_ent = tk.Entry(card, width=20, font=("Arial", 11), bg="#3d2b1f", fg="white", insertbackground="white")
        self.p_ent.grid(row=0, column=3, padx=15)

        tk.Label(card, text="Case Type:", bg=self.mahogany, fg="#F5F5DC").grid(row=0, column=4, sticky="w")
        self.t_box = ttk.Combobox(card, values=["Criminal", "Family", "Civil", "Corporate", "Others"], 
                                  state="readonly", width=18)
        self.t_box.grid(row=0, column=5, padx=15)
        self.t_box.current(0)

        # Functional Buttons
        btn_f = tk.Frame(self.root, bg=self.mahogany)
        btn_f.pack(pady=15)
        
        tk.Button(btn_f, text="FILE CASE", bg=self.gold, fg="#1A110B", font=("Arial", 10, "bold"), 
                  width=15, height=2, command=self.save_flow, cursor="hand2").grid(row=0, column=0, padx=10)
        
        tk.Button(btn_f, text="EDIT DETAILS", bg="#5D4037", fg="white", font=("Arial", 10, "bold"),
                  width=15, height=2, command=self.edit_flow, cursor="hand2").grid(row=0, column=1, padx=10)
        
        tk.Button(btn_f, text="WITHDRAW", bg="#8B0000", fg="white", font=("Arial", 10, "bold"),
                  width=15, height=2, command=self.drop, cursor="hand2").grid(row=0, column=2, padx=10)
        
        tk.Button(btn_f, text="REVIEW CASE", bg="#1A110B", fg=self.gold, font=("Arial", 10, "italic bold"),
                  width=25, height=2, command=lambda: LoginWindow(self.root), cursor="hand2").grid(row=0, column=3, padx=30)

        # Data Table with the requested Description Column
        cols = ("case id", "Client", "Type", "Case Description", "Status", "Reviewer")
        self.tree = ttk.Treeview(self.root, columns=cols, show="headings")
        
        # Configure column widths and alignment
        for col in cols:
            self.tree.heading(col, text=col.upper())
            if col == "Case Description":
                self.tree.column(col, anchor="w", width=350) # Wider for description text
            else:
                self.tree.column(col, anchor="center", width=130)

        # Status Coloring
        self.tree.tag_configure('Approved', background='#2E7D32', foreground='white')
        self.tree.tag_configure('Rejected', background='#C62828', foreground='white')
        
        self.tree.pack(fill="both", expand=True, padx=50, pady=25)

    def save_flow(self):
        # UI/UX: Prompt for description BEFORE authentication
        desc = simpledialog.askstring("Case Brief", "Enter additional details for your case (Optional):")
        if desc is None: return # User cancelled
        
        LoginWindow(self.root, on_success=lambda: [
            mongo.add_case(self.n_ent.get(), self.p_ent.get(), self.t_box.get(), desc or "No specific details provided."),
            self.refresh(),
            messagebox.showinfo("Success", "Legal case recorded successfully.")
        ])

    def edit_flow(self):
        selected = self.tree.selection()
        if not selected:
            return messagebox.showwarning("Selection", "Please select a case from the table to update.")
        
        new_desc = simpledialog.askstring("Edit Brief", "Update your case description:")
        if new_desc is None: return

        LoginWindow(self.root, on_success=lambda: [
            mongo.edit_case(selected[0], self.n_ent.get(), self.p_ent.get(), self.t_box.get(), new_desc),
            self.refresh(),
            messagebox.showinfo("Updated", "Case information has been modified.")
        ])

    def drop(self):
        selected = self.tree.selection()
        if selected and messagebox.askyesno("Confirm", "Are you sure you want to withdraw this legal case?"):
            mongo.delete_case(selected[0])
            self.refresh()

    def refresh(self):
        # Clear current rows
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Repopulate from MongoDB
        data = mongo.get_cases()
        for c in data:
            current_status = c.get('status', 'Pending')
            # Extract last 5 digits of ID for the "Password/ID" feel
            display_id = str(c['_id'])[-5:]
            
            self.tree.insert("", "end", iid=str(c['_id']), 
                             values=(display_id, 
                                     c['name'], 
                                     c['type'], 
                                     c.get('desc', 'N/A'), 
                                     current_status, 
                                     c.get('reviewed_by', 'None')), 
                             tags=(current_status,))

if __name__ == "__main__":
    root = tk.Tk()
    app = LegalManagementFirm(root)
    root.mainloop()