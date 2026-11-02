import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from modules.transaction import Transaction
from modules.budget import Budget
from modules.storage import DataStorage
from modules.analytics import FinancialAnalytics

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class FinTrackApp:

    def __init__(self, root):
        self.root = root
        self.root.title("FinTrack - Expense Manager")
        self.root.geometry("1150x750")
        self.root.minsize(950, 650)
        self.root.configure(bg="#111827")

        self.storage = DataStorage()
        self.transactions = self.storage.load_transactions()
        self.budgets = self.storage.load_budgets()

        self.setup_styles()
        self.create_layout()
        self.show_dashboard()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#1F2937",
            foreground="white",
            fieldbackground="#1F2937",
            rowheight=30,
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background="#374151",
            foreground="white",
            font=("Arial", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#047857")],
            foreground=[("selected", "white")]
        )

        style.configure(
            "TCombobox",
            fieldbackground="#1F2937",
            background="#374151",
            foreground="white"
        )

    def create_layout(self):
        self.sidebar = tk.Frame(
            self.root, bg="#0B1220", width=210
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="FinTrack",
            font=("Arial", 25, "bold"),
            fg="#34D399",
            bg="#0B1220"
        ).pack(pady=(30, 5))

        tk.Label(
            self.sidebar,
            text="PERSONAL FINANCE",
            font=("Arial", 9),
            fg="#9CA3AF",
            bg="#0B1220"
        ).pack(pady=(0, 35))

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Transactions", self.show_transactions),
            ("Budgets", self.show_budgets),
            ("Analytics", self.show_analytics)
        ]

        for name, command in buttons:
            tk.Button(
                self.sidebar,
                text="  " + name,
                command=command,
                font=("Arial", 12),
                fg="white",
                bg="#0B1220",
                activebackground="#047857",
                activeforeground="white",
                bd=0,
                anchor="w",
                padx=20,
                pady=15,
                cursor="hand2"
            ).pack(fill="x", padx=10, pady=4)

        self.content = tk.Frame(
            self.root, bg="#111827"
        )
        self.content.pack(
            side="left", fill="both", expand=True
        )

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def create_header(self, title):
        tk.Label(
            self.content,
            text=title,
            font=("Arial", 23, "bold"),
            fg="white",
            bg="#111827"
        ).pack(anchor="w", padx=30, pady=(25, 20))

    def get_analytics(self):
        return FinancialAnalytics(self.transactions)

    def create_card(self, parent, title, value, color):
        card = tk.Frame(parent, bg="#1F2937", padx=18, pady=18)
        card.pack(side="left", fill="both", expand=True, padx=8)

        tk.Label(
            card, text=title,
            font=("Arial", 11),
            fg="#9CA3AF",
            bg="#1F2937"
        ).pack(anchor="w")

        tk.Label(
            card, text=f"₹{value:,.2f}",
            font=("Arial", 20, "bold"),
            fg=color,
            bg="#1F2937"
        ).pack(anchor="w", pady=(12, 0))

    def show_dashboard(self):
        self.clear_content()
        self.create_header("Dashboard")

        summary = self.get_analytics().get_summary()

        cards = tk.Frame(self.content, bg="#111827")
        cards.pack(fill="x", padx=20)

        self.create_card(
            cards, "TOTAL INCOME",
            summary["income"], "#34D399"
        )

        self.create_card(
            cards, "TOTAL EXPENSES",
            summary["expenses"], "#F87171"
        )

        self.create_card(
            cards, "BALANCE",
            summary["balance"], "#60A5FA"
        )

        tk.Label(
            self.content,
            text="Recent Transactions",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#111827"
        ).pack(anchor="w", padx=30, pady=(30, 12))

        self.create_transaction_table(
            self.content, self.transactions[-5:]
        )

    def create_transaction_table(self, parent, records):
        columns = ("Date", "Title", "Category", "Type", "Amount")

        table = ttk.Treeview(
            parent, columns=columns, show="headings", height=9
        )

        for column in columns:
            table.heading(column, text=column)
            table.column(column, width=130, anchor="center")

        for transaction in reversed(records):
            table.insert(
                "",
                "end",
                values=(
                    transaction.transaction_date,
                    transaction.title,
                    transaction.category,
                    transaction.transaction_type,
                    f"₹{transaction.amount:,.2f}"
                )
            )

        table.pack(fill="x", padx=30, pady=5)

    def show_transactions(self):
        self.clear_content()
        self.create_header("Transactions")

        form = tk.Frame(self.content, bg="#1F2937", padx=15, pady=15)
        form.pack(fill="x", padx=30, pady=5)

        self.title_entry = self.create_entry(form, "Title")
        self.amount_entry = self.create_entry(form, "Amount")
        self.category_entry = self.create_entry(form, "Category")

        self.type_var = tk.StringVar(value="Expense")

        ttk.Combobox(
            form,
            textvariable=self.type_var,
            values=["Income", "Expense"],
            state="readonly",
            width=18
        ).pack(side="left", padx=8)

        tk.Button(
            form,
            text="Add Transaction",
            command=self.add_transaction,
            bg="#059669",
            fg="white",
            bd=0,
            padx=15,
            pady=9
        ).pack(side="left", padx=8)

        tk.Button(
            self.content,
            text="Delete Selected Transaction",
            command=self.delete_transaction,
            bg="#DC2626",
            fg="white",
            bd=0,
            padx=12,
            pady=9
        ).pack(anchor="e", padx=30, pady=10)

        self.transaction_table = ttk.Treeview(
            self.content,
            columns=("ID", "Date", "Title", "Category", "Type", "Amount"),
            show="headings",
            height=12
        )

        for col in ("ID", "Date", "Title", "Category", "Type", "Amount"):
            self.transaction_table.heading(col, text=col)
            self.transaction_table.column(col, width=110, anchor="center")

        self.transaction_table.pack(
            fill="both", expand=True, padx=30, pady=10
        )

        self.refresh_transaction_table()

    def create_entry(self, parent, placeholder):
        entry = tk.Entry(
            parent,
            font=("Arial", 11),
            bg="#374151",
            fg="white",
            insertbackground="white",
            relief="flat",
            width=17
        )
        entry.pack(side="left", padx=8, ipady=8)
        entry.insert(0, placeholder)
        return entry

    def add_transaction(self):
        title = self.title_entry.get().strip()
        amount = self.amount_entry.get().strip()
        category = self.category_entry.get().strip()
        transaction_type = self.type_var.get()

        if not title or not category or not amount:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        try:
            amount = float(amount)

            transaction = Transaction(
                title, amount, category, transaction_type
            )

            self.transactions.append(transaction)
            self.save_data()

            messagebox.showinfo(
                "Success", "Transaction added successfully!"
            )

            self.show_transactions()

        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))

    def refresh_transaction_table(self):
        for item in self.transaction_table.get_children():
            self.transaction_table.delete(item)

        for transaction in reversed(self.transactions):
            self.transaction_table.insert(
                "",
                "end",
                iid=transaction.transaction_id,
                values=(
                    transaction.transaction_id,
                    transaction.transaction_date,
                    transaction.title,
                    transaction.category,
                    transaction.transaction_type,
                    f"₹{transaction.amount:,.2f}"
                )
            )

    def delete_transaction(self):
        selected = self.transaction_table.selection()

        if not selected:
            messagebox.showwarning(
                "Selection", "Please select a transaction."
            )
            return

        transaction_id = selected[0]

        if not messagebox.askyesno(
            "Confirm", "Delete this transaction?"
        ):
            return

        self.transactions = [
            t for t in self.transactions
            if t.transaction_id != transaction_id
        ]

        self.save_data()
        self.show_transactions()
 
    def show_budgets(self):
        self.clear_content()
        self.create_header("Budget Management")

        form = tk.Frame(self.content, bg="#1F2937", padx=15, pady=15)
        form.pack(fill="x", padx=30, pady=10)

        category_entry = self.create_entry(form, "Category")
        limit_entry = self.create_entry(form, "Budget Limit")

        def add_budget():
            category = category_entry.get().strip()
            limit = limit_entry.get().strip()

            if not category or not limit:
                messagebox.showerror("Error", "Fill all fields.")
                return

            try:
                amount = float(limit)

                if amount <= 0:
                    raise ValueError("Budget must be greater than zero.")

                current = date.today()

                budget = Budget(
                    category,
                    amount,
                    current.month,
                    current.year
                )

                self.budgets = [
                    b for b in self.budgets
                    if not (
                        b.category.lower() == category.lower()
                        and b.month == current.month
                        and b.year == current.year
                    )
                ]

                self.budgets.append(budget)
                self.save_data()
                self.show_budgets()

                messagebox.showinfo(
                    "Success", "Budget saved successfully!"
                )

            except ValueError as error:
                messagebox.showerror("Invalid Input", str(error))

        tk.Button(
            form,
            text="Set Budget",
            command=add_budget,
            bg="#059669",
            fg="white",
            bd=0,
            padx=15,
            pady=9
        ).pack(side="left", padx=8)

        current = date.today()
        analytics = self.get_analytics()
        expenses = analytics.get_category_expenses()

        tk.Label(
            self.content,
            text="Current Month Budgets",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#111827"
        ).pack(anchor="w", padx=30, pady=20)

        for budget in self.budgets:
            if budget.month != current.month or budget.year != current.year:
                continue

            spent = float(expenses.get(budget.category, 0))
            remaining = budget.remaining_budget(spent)
            percentage = budget.usage_percentage(spent)

            card = tk.Frame(
                self.content, bg="#1F2937", padx=15, pady=12
            )
            card.pack(fill="x", padx=30, pady=6)

            tk.Label(
                card,
                text=f"{budget.category}  |  "
                    f"₹{spent:,.2f} / ₹{budget.limit_amount:,.2f}",
                fg="white",
                bg="#1F2937",
                font=("Arial", 11, "bold")
            ).pack(anchor="w")

            progress = ttk.Progressbar(
                card,
                maximum=100,
                value=min(percentage, 100)
            )
            progress.pack(fill="x", pady=8)

            status = (
                f"{percentage:.1f}% used | "
                f"₹{remaining:,.2f} remaining"
            )

            if remaining < 0:
                status += " | Budget exceeded!"

            tk.Label(
                card,
                text=status,
                fg="#F87171" if remaining < 0 else "#34D399",
                bg="#1F2937"
            ).pack(anchor="w")

            tk.Button(
                card,
                text="Delete Budget",
                command=lambda b=budget: self.delete_budget(b),
                bg="#DC2626",
                fg="white",
                bd=0,
                padx=12,
                pady=6,
                cursor="hand2"
            ).pack(anchor="e", pady=5)

    def delete_budget(self, budget):
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete the "
            f"{budget.category} budget?"
        )

        if confirm:
            self.budgets.remove(budget)
            self.save_data()
            self.show_budgets()

            messagebox.showinfo(
                "Success",
                "Budget deleted successfully!"
            )


    def show_analytics(self):
        self.clear_content()
        self.create_header("Financial Analytics")

        analytics = self.get_analytics()
        category_data = analytics.get_category_expenses()
        monthly_data = analytics.get_monthly_summary()

        figure = Figure(figsize=(9, 5), dpi=100)
        figure.patch.set_facecolor("#111827")

        ax1 = figure.add_subplot(121)
        ax2 = figure.add_subplot(122)

        ax1.set_facecolor("#1F2937")
        ax2.set_facecolor("#1F2937")

        if not category_data.empty:
            ax1.pie(
                category_data.values,
                labels=category_data.index,
                autopct="%1.1f%%",
                startangle=90
            )
            ax1.set_title(
                "Expense Distribution", color="white"
            )
        else:
            ax1.text(
                0.5, 0.5, "No expense data",
                color="white", ha="center"
            )

        if not monthly_data.empty:
            monthly_data.plot(
                kind="bar",
                ax=ax2,
                color=["#34D399", "#F87171"],
                width=0.7
            )
            ax2.set_title(
                "Monthly Income vs Expenses", color="white"
            )
            ax2.tick_params(axis="x", colors="white", rotation=30)
            ax2.tick_params(axis="y", colors="white")
            ax2.legend(facecolor="#1F2937", labelcolor="white")
            ax2.set_ylabel("Amount (₹)", color="white")
        else:
            ax2.text(
                0.5, 0.5, "No monthly data",
                color="white", ha="center"
            )

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(
            figure, master=self.content
        )
        canvas.draw()
        canvas.get_tk_widget().pack(
            fill="both", expand=True, padx=20, pady=10
        )

    def save_data(self):
        self.storage.save_data(
            self.transactions, self.budgets
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = FinTrackApp(root)
    root.mainloop()
