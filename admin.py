import tkinter as tk
from tkinter import ttk, messagebox
import mongo

class AdminDashboard:
    def __init__(self, parent_app, user):
        self.parent = parent_app
        self.user = user
        self.win = tk.Toplevel()
        self.win.title("STAFF CASE REVIEW PANEL")
        self.win.geometry("1150x750")
        self.win.configure(bg="#1A110B") # Mahogany luxury background
        
        # --- HEADER ---
        header_f = tk.Frame(self.win, bg="#000000", height=80)
        header_f.pack(fill="x")
        
        # Back Arrow for easy navigation
        tk.Button(header_f, text="← BACK TO PORTAL", font=("Arial", 10, "bold"),
                  bg="#000000", fg="#D4AF37", bd=0, cursor="hand2",
                  activebackground="#D4AF37", activeforeground="black",
                  command=self.win.destroy).pack(side="left", padx=20)
        
        tk.Label(header_f, text=f"OFFICIAL REVIEW | {user['role'].upper()}: {user['username'].upper()}", 
                 bg="#000000", fg="#D4AF37", font=("Times New Roman", 16, "bold")).pack(side="left", padx=20)

        # --- TABLE VIEW ---
        self.tree_frame = tk.Frame(self.win, bg="#1A110B")
        self.tree_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        cols = ("id", "Client", "Category", "Status", "Decision Log", "Strikes")
        self.tree = ttk.Treeview(self.tree_frame, columns=cols, show="headings")
        
        # Professional Luxury Styling
        style = ttk.Style()
        style.configure("Admin.Treeview", background="#2C1E16", foreground="white", fieldbackground="#2C1E16", rowheight=45)
        style.map("Admin.Treeview", background=[('selected', '#D4AF37')], foreground=[('selected', 'black')])
        self.tree.config(style="Admin.Treeview")

        for col in cols: 
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, anchor="center")
        
        self.tree.pack(fill="both", expand=True)
        
        # Status Color Coding
        self.tree.tag_configure("Approved", foreground="#D4AF37") # Gold
        self.tree.tag_configure("Solved", foreground="#28a745")   # Green
        self.tree.tag_configure("Rejected", foreground="#dc3545") # Red
        self.tree.tag_configure("Pending", foreground="#A89276")  # Muted Tan

        # --- CONTROL PANEL ---
        self.btn_f = tk.Frame(self.win, bg="#1A110B")
        self.btn_f.pack(pady=20)
        
        # Left Button: Logic changes based on selection
        self.action_btn_1 = tk.Button(self.btn_f, text="APPROVE CASE", bg="#28a745", fg="white", 
                                     font=("Arial", 10, "bold"), width=25, height=2, bd=0, 
                                     command=self.handle_approve_or_solve)
        self.action_btn_1.pack(side="left", padx=10)

        # Right Button: Logic changes based on selection
        self.action_btn_2 = tk.Button(self.btn_f, text="REJECT CASE", bg="#dc3545", fg="white", 
                                    font=("Arial", 10, "bold"), width=35, height=2, bd=0, 
                                    command=self.handle_reject_or_withdraw)
        self.action_btn_2.pack(side="left", padx=10)

        # Selection listener to update UI labels/buttons
        self.tree.bind("<<TreeviewSelect>>", self.update_ui_state)
        self.load()

    def load(self):
        """Standardizes the view and handles empty data."""
        for i in self.tree.get_children(): self.tree.delete(i)
        
        all_cases = mongo.get_cases()
        for c in all_cases:
            rc = c.get('rejection_count', 0)
            status = c['status']
            
            # Formulating the "Decision Log" column
            if status == "Approved":
                log = f"Approved by {c.get('reviewed_by', 'Staff')}"
            elif status == "Solved":
                log = f"Solved by {c.get('reviewed_by', 'Staff')}"
            elif rc == 1:
                log = "TAKE CASE (1st Rejection)"
            else:
                log = "Awaiting Initial Review"

            self.tree.insert("", "end", iid=str(c['_id']), 
                             values=(str(c['_id'])[-5:], c['name'], c['type'], status, log, rc),
                             tags=(status,))

    def update_ui_state(self, event=None):
        """Dynamically switches button functionality based on case status."""
        sel = self.tree.selection()
        if not sel: return
        
        case_id = sel[0]
        case = next(c for c in mongo.get_cases() if str(c['_id']) == case_id)
        status = case.get('status')
        rc = case.get('rejection_count', 0)

        # DEFAULT STATES
        self.action_btn_1.config(state="normal", text="APPROVE CASE", bg="#28a745")
        self.action_btn_2.config(state="normal", text="REJECT (SEND TO ANOTHER)", bg="#dc3545", fg="white")

        if status == "Approved":
            self.action_btn_1.config(text="MARK CASE SOLVED", bg="#17a2b8")
            self.action_btn_2.config(text="WITHDRAW RECORD", bg="#6c757d")
        
        elif status == "Solved":
            self.action_btn_1.config(text="RECORD SEALED (SOLVED)", state="disabled", bg="#004d40")
            self.action_btn_2.config(text="DELETE ARCHIVE", bg="#000000")

        elif rc == 1:
            self.action_btn_1.config(text="APPROVE (LAWYER TAKEOVER)")
            self.action_btn_2.config(text="PERMANENTLY DELETE", bg="#000000", fg="#dc3545")

    def handle_approve_or_solve(self):
        sel = self.tree.selection()
        if not sel: return
        
        case_id = sel[0]
        case = next(c for c in mongo.get_cases() if str(c['_id']) == case_id)
        status = case.get('status')

        if status == "Approved":
            if messagebox.askyesno("Final Verdict", "Mark this case as SOLVED and successful?"):
                mongo.update_status(case_id, "Solved", self.user['username'])
                self.refresh_all()
        else:
            if messagebox.askyesno("Confirm Approval", "Approve this case? It will be locked for editing."):
                mongo.update_status(case_id, "Approved", self.user['username'])
                self.refresh_all()

    def handle_reject_or_withdraw(self):
        sel = self.tree.selection()
        if not sel: return
        
        case_id = sel[0]
        case = next(c for c in mongo.get_cases() if str(c['_id']) == case_id)
        status = case.get('status')
        rc = case.get('rejection_count', 0)

        if status == "Approved" or status == "Solved":
            if messagebox.askyesno("Warning", "Withdraw this record? It will be removed from the Vault."):
                mongo.delete_case(case_id)
                self.refresh_all()
        elif rc >= 1:
            if messagebox.askyesno("Critical", "Second rejection detected. Purge record permanently?"):
                mongo.delete_case(case_id)
                self.refresh_all()
        else:
            if messagebox.askyesno("Reject", "Reject this case? Another lawyer can still take it."):
                mongo.increment_rejection(case_id)
                self.refresh_all()

    def refresh_all(self):
        self.load()
        # Refreshes the parent (main dashboard) in the background
        if self.parent:
            self.parent.refresh()
        messagebox.showinfo("Vault Synced", "Records have been successfully updated.")