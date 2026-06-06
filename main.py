import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
 
 #transaction 
 #fix date -done
class Transaction:
    def __init__(self, type, category, amount):
        self.date = date.today()
        self.type = type
        self.category = category
        self.amount = amount
 
    def __str__(self):
        return f"{self.date} | {self.type} | {self.category} | Rs.{self.amount}"
 
    def to_csv(self):
        return f"{self.date},{self.type},{self.category},{self.amount}\n"
 
 
class Tracker:
    def __init__(self):
        self.__transactions = []
        self.__balance = 0
        self.load_from_file()
 
    def add_income(self, amount, category):
        t = Transaction("Income", category, amount)
        self.__transactions.append(t)
        self.__balance += amount
        self.save_to_file()
 
    def add_expense(self, amount, category):
        t = Transaction("Expense", category, amount)
        self.__transactions.append(t)
        self.__balance -= amount
        self.save_to_file()
 
    def get_balance(self):
        return self.__balance
 
    def get_transactions(self):
        return self.__transactions
 
    def save_to_file(self):
        with open("transactions.txt", "w") as f:
            for t in self.__transactions:
                f.write(t.to_csv())
 
    def load_from_file(self):
        try:
            with open("transactions.txt", "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 4:
                        date_str, type_, category, amount = parts
                        t = Transaction(type_, category, float(amount))
                        t.date = date_str
                        self.__transactions.append(t)
                        if type_ == "Income":
                            self.__balance += float(amount)
                        else:
                            self.__balance -= float(amount)
        except FileNotFoundError:
            pass
 
 
class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Personal Finance Tracker")
        self.root.geometry("650x600")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)
 
        self.tracker = Tracker()
        self.build_ui()
        self.refresh_transactions()
 
    def build_ui(self):
        # ── Title
        tk.Label(
            self.root, text="💰 Personal Finance Tracker",
            font=("Helvetica", 18, "bold"),
            bg="#1e1e2e", fg="#cdd6f4"
        ).pack(pady=15)
 
        # ── Balance card
        self.balance_frame = tk.Frame(self.root, bg="#313244", pady=10)
        self.balance_frame.pack(fill="x", padx=20)
 
        tk.Label(
            self.balance_frame, text="Current Balance",
            font=("Helvetica", 11), bg="#313244", fg="#a6adc8"
        ).pack()
 
        self.balance_label = tk.Label(
            self.balance_frame, text=f"Rs.{self.tracker.get_balance()}",
            font=("Helvetica", 24, "bold"),
            bg="#313244", fg="#a6e3a1"
        )
        self.balance_label.pack()
 
        # ── Input section
        input_frame = tk.Frame(self.root, bg="#1e1e2e")
        input_frame.pack(fill="x", padx=20, pady=15)
 
        # Amount
        tk.Label(
            input_frame, text="Amount (Rs.)",
            font=("Helvetica", 10), bg="#1e1e2e", fg="#a6adc8"
        ).grid(row=0, column=0, sticky="w", pady=3)
 
        self.amount_entry = tk.Entry(
            input_frame, font=("Helvetica", 12),
            bg="#313244", fg="#cdd6f4",
            insertbackground="#cdd6f4", relief="flat", width=20
        )
        self.amount_entry.grid(row=1, column=0, padx=(0, 10), ipady=6)
 
        # Category
        tk.Label(
            input_frame, text="Category",
            font=("Helvetica", 10), bg="#1e1e2e", fg="#a6adc8"
        ).grid(row=0, column=1, sticky="w", pady=3)
 
        self.category_var = tk.StringVar(value="Food")
        categories = ["Food", "Salary", "Rent", "Transport", "Shopping", "Entertainment", "Other"]
        self.category_menu = ttk.Combobox(
            input_frame, textvariable=self.category_var,
            values=categories, font=("Helvetica", 12), width=17, state="readonly"
        )
        self.category_menu.grid(row=1, column=1, padx=(0, 10), ipady=4)
 
        # Buttons
        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.pack(pady=5)
 
        tk.Button(
            btn_frame, text="➕ Add Income",
            font=("Helvetica", 11, "bold"),
            bg="#a6e3a1", fg="#1e1e2e",
            relief="flat", padx=20, pady=8,
            cursor="hand2",
            command=self.add_income
        ).grid(row=0, column=0, padx=10)
 
        tk.Button(
            btn_frame, text="➖ Add Expense",
            font=("Helvetica", 11, "bold"),
            bg="#f38ba8", fg="#1e1e2e",
            relief="flat", padx=20, pady=8,
            cursor="hand2",
            command=self.add_expense
        ).grid(row=0, column=1, padx=10)
 
        tk.Button(
            btn_frame, text="🗑 Clear All",
            font=("Helvetica", 11, "bold"),
            bg="#585b70", fg="#cdd6f4",
            relief="flat", padx=20, pady=8,
            cursor="hand2",
            command=self.clear_all
        ).grid(row=0, column=2, padx=10)
 
        # ── Transactions table
        tk.Label(
            self.root, text="Transaction History",
            font=("Helvetica", 12, "bold"),
            bg="#1e1e2e", fg="#cdd6f4"
        ).pack(pady=(15, 5))
 
        table_frame = tk.Frame(self.root, bg="#1e1e2e")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
 
        # style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
            background="#313244",
            foreground="#cdd6f4",
            fieldbackground="#313244",
            font=("Helvetica", 10),
            rowheight=28
        )
        style.configure("Treeview.Heading",
            background="#45475a",
            foreground="#cdd6f4",
            font=("Helvetica", 10, "bold")
        )
        style.map("Treeview", background=[("selected", "#585b70")])
 
        self.tree = ttk.Treeview(
            table_frame,
            columns=("date", "type", "category", "amount"),
            show="headings", height=12
        )
        self.tree.heading("date", text="Date")
        self.tree.heading("type", text="Type")
        self.tree.heading("category", text="Category")
        self.tree.heading("amount", text="Amount")
 
        self.tree.column("date", width=110, anchor="center")
        self.tree.column("type", width=90, anchor="center")
        self.tree.column("category", width=130, anchor="center")
        self.tree.column("amount", width=120, anchor="center")
 
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
 
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
 
    def add_income(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive!")
                return
            category = self.category_var.get()
            self.tracker.add_income(amount, category)
            self.amount_entry.delete(0, tk.END)
            self.refresh_transactions()
            self.update_balance(income=True)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
 
    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive!")
                return
            if amount > self.tracker.get_balance():
                messagebox.showerror("Error", "Not enough balance!")
                return
            category = self.category_var.get()
            self.tracker.add_expense(amount, category)
            self.amount_entry.delete(0, tk.END)
            self.refresh_transactions()
            self.update_balance(income=False)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
 
    def update_balance(self, income=True):
        balance = self.tracker.get_balance()
        self.balance_label.config(
            text=f"Rs.{balance:.2f}",
            fg="#a6e3a1" if balance >= 0 else "#f38ba8"
        )
 
    def refresh_transactions(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
 
        for t in reversed(self.tracker.get_transactions()):
            color = "income" if t.type == "Income" else "expense"
            self.tree.insert("", "end",
                values=(t.date, t.type, t.category, f"Rs.{float(t.amount):.2f}"),
                tags=(color,)
            )
 
        self.tree.tag_configure("income", foreground="#a6e3a1")
        self.tree.tag_configure("expense", foreground="#f38ba8")
        self.update_balance()
 
    def clear_all(self):
        confirm = messagebox.askyesno("Clear All", "Delete all transactions?")
        if confirm:
            open("transactions.txt", "w").close()
            self.tracker = Tracker()
            self.refresh_transactions()
 
 
 
if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
 
