import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mongo
from login import LoginWindow
from signup import SignupWindow
from admin import AdminDashboard

# --- 1. THE INITIAL GATEWAY ---
class AuthGateway:
    def __init__(self, parent, on_success):
        self.win = tk.Toplevel(parent)
        self.win.title("SYSTEM ACCESS")
        self.win.geometry("400x350")
        self.win.configure(bg="#1A110B")
        self.on_success = on_success

        tk.Label(self.win, text="SELECT ACCESS PORTAL", font=("Times New Roman", 16, "bold"), 
                 bg="#1A110B", fg="#D4AF37").pack(pady=40)

        tk.Button(self.win, text="CLIENT PORTAL", bg="#D4AF37", fg="black", font=("Arial", 10, "bold"),
                  width=25, height=2, bd=0, cursor="hand2", 
                  command=lambda: self.select_role(False)).pack(pady=10)

        tk.Button(self.win, text="STAFF PORTAL", bg="#2C1E16", fg="#D4AF37", font=("Arial", 10, "bold"),
                  width=25, height=2, bd=0, cursor="hand2", 
                  command=lambda: self.select_role(True)).pack(pady=10)

    def select_role(self, is_admin):
        self.win.destroy()
        PortalChoice(self.win.master, is_admin, self.on_success)

# --- 2. THE LOGIN/SIGNUP CHOICE ---
class PortalChoice:
    def __init__(self, parent, is_admin, on_success):
        self.win = tk.Toplevel(parent)
        self.win.title("SECURE ENTRY")
        self.win.geometry("400x320")
        self.win.configure(bg="#1A110B")
        self.is_admin = is_admin
        self.on_success = on_success

        role_text = "STAFF" if is_admin else "CLIENT"
        tk.Label(self.win, text=f"{role_text} OPTIONS", font=("Times New Roman", 14, "bold"), 
                 bg="#1A110B", fg="#D4AF37").pack(pady=30)

        tk.Button(self.win, text="I HAVE AN ACCOUNT (LOG IN)", bg="#D4AF37", fg="black", 
                  font=("Arial", 9, "bold"), width=28, height=2, bd=0, 
                  command=self.open_login).pack(pady=10)

        tk.Button(self.win, text="NEW MEMBER (SIGN UP)", bg="#2C1E16", fg="white", 
                  font=("Arial", 9, "bold"), width=28, height=2, bd=0, 
                  command=self.open_signup).pack(pady=10)

    def open_login(self):
        self.win.destroy()
        LoginWindow(self.win.master, on_success=self.on_success)

    def open_signup(self):
        self.win.destroy()
        SignupWindow(self.win.master, is_admin=self.is_admin, on_success=self.on_success)

# --- 3. EDIT DIALOG ---
class EditDialog:
    def __init__(self, parent, case_data, callback):
        self.win = tk.Toplevel(parent)
        self.win.title("Update Case Record")
        self.win.geometry("450x650")
        self.win.configure(bg="#1A110B")
        self.callback = callback

        tk.Label(self.win, text="MODIFY LEGAL RECORD", font=("Times New Roman", 18, "bold"), 
                 bg="#1A110B", fg="#D4AF37").pack(pady=25)

        f = tk.Frame(self.win, bg="#1A110B")
        f.pack(padx=40, fill="both")

        tk.Label(f, text="Client Name:", bg="#1A110B", fg="white").pack(anchor="w")
        self.n = tk.Entry(f, width=40, bg="#2C1E16", fg="white", borderwidth=0, insertbackground="#D4AF37")
        self.n.insert(0, case_data['name']); self.n.pack(pady=5, ipady=3)

        tk.Label(f, text="Contact Phone:", bg="#1A110B", fg="white").pack(anchor="w", pady=(10,0))
        self.p = tk.Entry(f, width=40, bg="#2C1E16", fg="white", borderwidth=0, insertbackground="#D4AF37")
        self.p.insert(0, case_data['phone']); self.p.pack(pady=5, ipady=3)

        tk.Label(f, text="Case Category:", bg="#1A110B", fg="white").pack(anchor="w", pady=(10,0))
        self.t = ttk.Combobox(f, values=["Criminal", "Civil", "Family", "Corporate", "Others"], width=37)
        self.t.set(case_data['type']); self.t.pack(pady=5)

        tk.Label(f, text="Case Brief:", bg="#1A110B", fg="white").pack(anchor="w", pady=(10,0))
        self.d = tk.Text(f, width=40, height=8, bg="#2C1E16", fg="white", borderwidth=0, insertbackground="#D4AF37")
        self.d.insert("1.0", case_data['desc']); self.d.pack(pady=5)

        tk.Button(self.win, text="SAVE CHANGES", bg="#D4AF37", fg="black", font=("Arial", 10, "bold"),
                  width=25, command=self.save, cursor="hand2", bd=0).pack(pady=30)

    def save(self):
        self.callback(self.n.get(), self.p.get(), self.t.get(), self.d.get("1.0", "end-1c"))
        self.win.destroy()

# --- 4. MAIN DASHBOARD ---
class LegalFirmPortal:
    def __init__(self, root):
        self.root = root
        self.root.title("LEGAL MANAGEMENT SYSTEM")
        self.root.geometry("1400x850") 
        self.root.configure(bg="#1A110B")
        
        self.gold, self.mahogany = "#D4AF37", "#2C1E16"
        self.current_session = None 
        
        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        # --- TOP HEADER NAVIGATION ---
        self.nav = tk.Frame(self.root, bg="#000000", height=100)
        self.nav.pack(fill="x")
        tk.Label(self.nav, text="L E G A L  M A N A G E M E N T", font=("Times New Roman", 26, "bold"), 
                 bg="#000000", fg=self.gold).pack(side="left", padx=50, pady=25)

        self.auth_frame = tk.Frame(self.nav, bg="#000000")
        self.auth_frame.pack(side="right", padx=50)

        # --- FILING FORM ---
        self.entry_f = tk.LabelFrame(self.root, text=" FILE NEW CASE RECORD ", bg=self.mahogany, 
                                fg=self.gold, font=("Arial", 10, "bold"), padx=25, pady=15)
        self.entry_f.pack(fill="x", padx=60, pady=(20, 10))
        
        tk.Label(self.entry_f, text="Client Name:", bg=self.mahogany, fg="white").grid(row=0, column=0)
        self.n_ent = tk.Entry(self.entry_f, width=20, bg="#1A110B", fg="white", borderwidth=0); self.n_ent.grid(row=0, column=1, padx=5)
        
        tk.Label(self.entry_f, text="Contact:", bg=self.mahogany, fg="white").grid(row=0, column=2)
        self.p_ent = tk.Entry(self.entry_f, width=15, bg="#1A110B", fg="white", borderwidth=0); self.p_ent.grid(row=0, column=3, padx=5)
        
        tk.Label(self.entry_f, text="Type:", bg=self.mahogany, fg="white").grid(row=0, column=4)
        self.t_box = ttk.Combobox(self.entry_f, values=["Criminal", "Civil", "Family", "Corporate", "others"], width=15, state="readonly")
        self.t_box.grid(row=0, column=5, padx=10); self.t_box.current(0)
        
        tk.Button(self.entry_f, text="FILE CASE", bg=self.gold, fg="black", font=("Arial", 9, "bold"), 
                  width=12, command=self.file_flow, cursor="hand2", bd=0).grid(row=0, column=6, padx=20)

        # --- ACTION WORKBAR INTERFACE ---
        self.action_bar = tk.Frame(self.root, bg="#1A110B")
        self.action_bar.pack(fill="x", padx=60, pady=10)
        
        tk.Button(self.action_bar, text="EDIT RECORD", bg=self.mahogany, fg=self.gold, 
                  font=("Arial", 9, "bold"), width=20, bd=0, command=self.edit_flow).pack(side="left", padx=5)
        
        tk.Button(self.action_bar, text="WITHDRAW RECORD", bg="#721c24", fg="white", 
                  font=("Arial", 9, "bold"), width=20, bd=0, command=self.withdraw_flow).pack(side="left", padx=5)
        
        tk.Button(self.action_bar, text="REVIEW CASE (STAFF)", bg=self.gold, fg="black", 
                  font=("Arial", 9, "bold"), width=20, bd=0, command=self.review_gate).pack(side="left", padx=5)
        
        self.render_nav_buttons()

        # --- FIXED BOTTOM FOOTER ---
        self.footer = tk.Frame(self.root, bg="#000000", height=50)
        self.footer.pack(side="bottom", fill="x")
        
        contact_txt = "location: 256 pangani,Nairobi  |    Emergency Counsel: +1 (555) 900-LEGAL   |   email: L.m.f @legalfirm.com"
        tk.Label(self.footer, text=contact_txt, font=("Arial", 9), bg="#000000", fg="#A89276").pack(pady=15)

        # Container Workspace for structural adjustments
        self.workspace = tk.Frame(self.root, bg="#1A110B")
        self.workspace.pack(fill="both", expand=True, padx=60, pady=(0, 20))

        # --- SHIELDED CONFIDENTIAL SPLIT LANDING LAYOUT ---
        self.splash_frame = tk.Frame(self.workspace, bg="#2C1E16", highlightbackground=self.gold, highlightthickness=1)
        
        # LEFT COLUMN FRAME: Handled natively via scalable UI parameters
        left_img_column = tk.Frame(self.splash_frame, bg="#2C1E16", width=500)
        left_img_column.pack(side="left", fill="both", expand=True, padx=(40, 20), pady=30)
        
        # Scalable Vector Unicode character configuration mapping
        self.img_lbl = tk.Label(left_img_column, text="⚖", font=("Times New Roman", 110), bg="#2C1E16", fg=self.gold)
        self.img_lbl.pack(expand=True)

        # RIGHT COLUMN FRAME: Designed exclusively for About Content and Actions
        right_info_column = tk.Frame(self.splash_frame, bg="#2C1E16")
        right_info_column.pack(side="right", fill="both", expand=True, padx=(20, 40), pady=30)

        tk.Label(right_info_column, text="LEGAL RECORDS MANAGEMENT", font=("Times New Roman", 24, "bold"), bg="#2C1E16", fg=self.gold, anchor="w").pack(fill="x", pady=(20, 5))
        
        about_card = tk.Frame(right_info_column, bg="#1A110B", bd=1, relief="solid")
        about_card.pack(fill="x", pady=15)
        
        about_body = (
            "Welcome to our legal management firm. We specialize in family law , personal injury cases,corporate litigation,criminal defense and any other legal matters."
        )
        tk.Label(about_card, text="ABOUT US", font=("Times New Roman", 12, "bold"), bg="#1A110B", fg=self.gold, anchor="w").pack(fill="x", padx=25, pady=(15, 5))
        tk.Label(about_card, text=about_body, font=("Arial", 10), bg="#1A110B", fg="white", wraplength=550, justify="left").pack(padx=25, pady=(0, 20))
        
        tk.Button(right_info_column, text="LOGIN ", font=("Arial", 10, "bold"), bg=self.gold, fg="black", bd=0, padx=25, pady=12, command=self.login_trigger).pack(anchor="w", pady=10)

        # --- MAIN SECURE DATA TREEVIEW ---
        cols = ("id", "Client", "Type", "Contact", "Brief", "Status", "Reviewer")
        self.tree = ttk.Treeview(self.workspace, columns=cols, show="headings")
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=self.mahogany, foreground="white", fieldbackground=self.mahogany, rowheight=40)
        style.configure("Treeview.Heading", background="#000000", foreground=self.gold)
        
        for col in cols:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, anchor="center", width=100)
        self.tree.column("Brief", width=350)

    def render_nav_buttons(self):
        for w in self.auth_frame.winfo_children(): w.destroy()
        if not self.current_session:
            tk.Button(self.auth_frame, text="LOGIN/SIGN UP", bg=self.gold, fg="black", 
                      font=("Arial", 9, "bold"), width=18, bd=0, cursor="hand2",
                      command=self.login_trigger).pack(padx=5)
            self.n_ent.config(state="normal")
        else:
            name = self.current_session['username'].upper()
            tk.Label(self.auth_frame, text=f"WELCOME, {name}", bg="#000000", 
                     fg=self.gold, font=("Arial", 9)).pack(side="left", padx=10)
            tk.Button(self.auth_frame, text="LOG OUT", bg="#721c24", fg="white", 
                      font=("Arial", 9, "bold"), bd=0, command=self.logout).pack(side="right")
            
            if self.current_session['role'] == "Client":
                self.n_ent.delete(0, 'end')
                self.n_ent.insert(0, self.current_session['username'])
                self.n_ent.config(state="disabled")

    def refresh(self):
        """Swaps layout workspace contexts depending on active authentication."""
        if not self.current_session:
            self.tree.pack_forget()
            self.splash_frame.pack(fill="both", expand=True, pady=20)
            return
        
        self.splash_frame.pack_forget()
        self.tree.pack(fill="both", expand=True)

        for i in self.tree.get_children(): self.tree.delete(i)
        for c in mongo.get_cases():
            auth = False
            curr_user = str(self.current_session['username']).strip().lower()
            case_owner = str(c['name']).strip().lower()
            
            if curr_user == case_owner or self.current_session['role'] != "Client":
                auth = True
        
            if auth:
                self.tree.insert("", "end", iid=str(c['_id']), values=(
                    str(c['_id'])[-5:], c['name'], c['type'], c['phone'], c['desc'], c['status'], c.get('reviewed_by', 'None')
                ))

    def login_trigger(self): 
        AuthGateway(self.root, on_success=self.login_success)

    def login_success(self, user): 
        self.current_session = user
        self.render_nav_buttons()
        self.refresh()

    def logout(self): 
        self.current_session = None
        self.n_ent.config(state="normal") 
        self.n_ent.delete(0, 'end')
        self.render_nav_buttons()
        self.refresh()

    def review_gate(self):
        if not self.current_session:
            messagebox.showinfo("Staff Required", "Please verify your Staff credentials to enter the Review portal.")
            PortalChoice(self.root, is_admin=True, on_success=self.login_success)
        elif self.current_session['role'] == "Client":
            messagebox.showerror("Access Denied", "Unauthorized Access: The administrative review panel is restricted to firm staff.")
        else:
            AdminDashboard(self, self.current_session)

    def edit_flow(self):
        if not self.current_session: 
            messagebox.showwarning("Auth Required", "Please login to access case modification tools.")
            return self.login_trigger()
            
        sel = self.tree.selection()
        if not sel: return messagebox.showwarning("Selection", "Select a record.")
            
        case = next((c for c in mongo.get_cases() if str(c['_id']) == sel[0]), None)
        if case:
            curr = self.current_session['username'].strip().lower()
            owner = case['name'].strip().lower()
            if curr == owner or self.current_session['role'] != "Client":
                EditDialog(self.root, case, lambda n, p, t, d: [mongo.update_case(sel[0], n, p, t, d), self.refresh()])
            else:
                messagebox.showerror("Denied", "Ownership verification failed.")

    def withdraw_flow(self):
        if not self.current_session: 
            return self.login_trigger()
            
        sel = self.tree.selection()
        if not sel: return
        
        case = next((c for c in mongo.get_cases() if str(c['_id']) == sel[0]), None)
        if case:
            curr = self.current_session['username'].strip().lower()
            owner = case['name'].strip().lower()
            
            if curr == owner or self.current_session['role'] != "Client":
                if self.current_session['role'] == "Client" and case['status'] not in ["Pending", "Rejected"]:
                    messagebox.showerror("Vault Sealed", f"Withdrawal Denied: Case file has already been '{case['status']}' and cannot be altered.")
                    return
                
                if messagebox.askyesno("Confirm", "Are you sure you want to withdraw this legal record?"):
                    mongo.delete_case(sel[0])
                    self.refresh()
            else:
                messagebox.showerror("Denied", "Ownership verification failed.")

    def file_flow(self):
        if not self.current_session:
            messagebox.showwarning("Authentication Required", "To file an official case brief, you must login or register a client account.")
            AuthGateway(self.root, on_success=self.login_success)
            return

        n, p = self.n_ent.get(), self.p_ent.get()
        if n and p:
            d = simpledialog.askstring("Case Brief", f"Enter details for {n}:")
            if d: 
                mongo.add_case(n, p, self.t_box.get(), d)
                self.refresh()
                self.p_ent.delete(0, 'end')

if __name__ == "__main__":
    root = tk.Tk()
    app = LegalFirmPortal(root)
    root.mainloop()