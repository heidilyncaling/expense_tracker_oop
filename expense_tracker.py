import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import calendar
import datetime

# Expense class
class Expense:
    def __init__(self, name, amount, category):
        self.name = name
        self.amount = amount
        self.category = category

# Budget planner
class BudgetPlanner:
    def get_monthly_budget(self, allowance, is_daily):
        days = calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1]
        return allowance * days if is_daily else allowance

# Manages saving/loading
class ExpenseManager:
    def __init__(self, file_path="expenses.csv"):
        self.file_path = file_path

    def save_expense(self, expense):
        with open(self.file_path, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([expense.name, expense.amount, expense.category])

    def reset_expenses(self):
        open(self.file_path, "w").close()

    def load_expenses(self):
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, newline="", encoding="utf-8") as file:
            return list(csv.reader(file))

# Main App
class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expenses Tracker")
        self.root.geometry("440x620")
        self.root.configure(bg="#FFEDA2")

        self.expense_manager = ExpenseManager()
        self.budget_planner = BudgetPlanner()
        self.monthly_budget = 0.0

        self.categories = [
            "🍔 Food", "🚌 Transport", "🧾 Bills", "🏥 Health",
            "💅 Personal Care", "🎓 Education", "🎮 Entertainment",
            "🎁 Gifts", "🛍️ Shopping", "✈️ Travel", "💸 Debt", "💰 Savings"
        ]

        self.font_header = ("DM Serif Display", 20, "bold")
        self.font_label = ("DM Serif Display", 12)
        self.font_button = ("DM Serif Display", 11)

        self.build_gui()

    def build_gui(self):
        # Header
        tk.Label(self.root, text="Expenses Tracker", bg="#FFEDA2", fg="#4282AA",
                 font=self.font_header).pack(pady=15)

        # Budget input
        tk.Label(self.root, text="Set Your Allowance (₱)", bg="#FFEDA2", font=self.font_label).pack()
        self.allowance_entry = tk.Entry(self.root, font=self.font_label)
        self.allowance_entry.pack(pady=5)

        self.is_daily = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Daily Allowance", bg="#FFEDA2", variable=self.is_daily,
                       font=self.font_label).pack()

        tk.Button(self.root, text="Set Budget", bg="#4282AA", fg="white", font=self.font_button,
                  command=self.set_budget).pack(pady=8)

        self.budget_label = tk.Label(self.root, text="Remaining Budget: ₱0.00",
                                     bg="#FFEDA2", font=self.font_label, fg="#333")
        self.budget_label.pack(pady=10)

        # Expense form
        form_frame = tk.Frame(self.root, bg="#FFEDA2")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Expense Name:", bg="#FFEDA2", font=self.font_label).grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(form_frame, font=self.font_label)
        self.name_entry.grid(row=0, column=1)

        tk.Label(form_frame, text="Amount (₱):", bg="#FFEDA2", font=self.font_label).grid(row=1, column=0, sticky="w")
        self.amount_entry = tk.Entry(form_frame, font=self.font_label)
        self.amount_entry.grid(row=1, column=1)

        tk.Label(form_frame, text="Category:", bg="#FFEDA2", font=self.font_label).grid(row=2, column=0, sticky="w")
        self.category_var = tk.StringVar()
        self.category_menu = ttk.Combobox(form_frame, textvariable=self.category_var, values=self.categories,
                                          font=self.font_label, state="readonly")
        self.category_menu.grid(row=2, column=1)

        # Buttons
        button_frame = tk.Frame(self.root, bg="#FFEDA2")
        button_frame.pack(pady=15)

        tk.Button(button_frame, text="➕ Add Expense", bg="#4282AA", fg="white", font=self.font_button,
                  width=18, command=self.add_expense).grid(row=0, column=0, padx=5, pady=5)

        tk.Button(button_frame, text="📊 Show Summary", bg="#4282AA", fg="white", font=self.font_button,
                  width=18, command=self.show_summary).grid(row=1, column=0, padx=5, pady=5)

        tk.Button(button_frame, text="🧹 Reset All", bg="#d9534f", fg="white", font=self.font_button,
                  width=18, command=self.reset_expenses).grid(row=2, column=0, padx=5, pady=5)

    def set_budget(self):
        try:
            allowance = float(self.allowance_entry.get())
            self.monthly_budget = self.budget_planner.get_monthly_budget(allowance, self.is_daily.get())
            self.update_budget_label()
            messagebox.showinfo("Budget Set", f"Your monthly budget: ₱{self.monthly_budget:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def add_expense(self):
        name = self.name_entry.get().strip()
        category = self.category_var.get()

        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
            return

        if not name or not category:
            messagebox.showerror("Error", "Please fill out all fields.")
            return

        expense = Expense(name, amount, category)
        self.expense_manager.save_expense(expense)
        self.monthly_budget -= amount
        self.update_budget_label()

        messagebox.showinfo("Saved", f"Saved {name} - ₱{amount:.2f}")
        self.name_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_menu.set("")

    def show_summary(self):
        expenses = self.expense_manager.load_expenses()
        total = 0.0
        for row in expenses:
            try:
                total += float(row[1])
            except:
                continue
        remaining = self.monthly_budget
        messagebox.showinfo("Summary", f"🧾 Total Spent: ₱{total:.2f}\n💰 Remaining: ₱{remaining:.2f}")

    def reset_expenses(self):
        self.expense_manager.reset_expenses()
        self.monthly_budget = 0.0
        self.update_budget_label()
        messagebox.showinfo("Reset", "All expenses cleared!")

    def update_budget_label(self):
        self.budget_label.config(text=f"Remaining Budget: ₱{self.monthly_budget:.2f}")

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()
    