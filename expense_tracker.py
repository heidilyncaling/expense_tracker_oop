# expense.py
class Expense:
    def __init__(self, name: str, amount: float, category: str):
        self.name = name
        self.amount = amount
        self.category = category

    def __repr__(self):
        return f"<Expense: {self.name}, {self.category}, ₱{self.amount:.2f}>"


# manager.py
import calendar
import datetime
from expense import Expense

class ExpenseManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.expenses: list[Expense] = []

    def reset(self):
        with open(self.file_path, "w") as file:
            pass
        print("\u2705 All expenses have been reset.\n")

    def load_expenses(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    name, amount, category = line.strip().split(",")
                    self.expenses.append(Expense(name, float(amount), category))
        except FileNotFoundError:
            print("No expense file found yet.")
        except Exception as error:
            print(f"Error reading file: {error}")

    def save_expense(self, expense: Expense):
        print(f"Saving Expense: {expense} to {self.file_path}")
        with open(self.file_path, "a", encoding="utf-8") as file:
            file.write(f"{expense.name},{expense.amount},{expense.category}\n")

    def summarize(self, budget: float):
        expenses_by_category = {}
        for expense in self.expenses:
            expenses_by_category[expense.category] = expenses_by_category.get(expense.category, 0) + expense.amount

        print("Expenses By Category:")
        for category, total in expenses_by_category.items():
            print(f"  {category}: ₱{total:.2f}")

        total_spent = sum(expense.amount for expense in self.expenses)
        remaining_budget = budget - total_spent

        print(f"Total Spent: ₱{total_spent:.2f}")
        print(f"Budget Remaining: ₱{remaining_budget:.2f}")

        current_date = datetime.datetime.now()
        days_left = calendar.monthrange(current_date.year, current_date.month)[1] - current_date.day

        if days_left > 0:
            daily_budget = remaining_budget / days_left
            print(f"Budget Per Day: ₱{daily_budget:.2f}")
        else:
            print("Month is ending today. Plan next month's budget!")


# budget.py
from abc import ABC, abstractmethod

class BudgetStrategy(ABC):
    @abstractmethod
    def calculate_budget(self, amount: float) -> float:
        pass


class MonthlyBudget(BudgetStrategy):
    def calculate_budget(self, amount: float) -> float:
        return amount


class DailyBudget(BudgetStrategy):
    def calculate_budget(self, amount: float) -> float:
        current_date = datetime.datetime.now()
        days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
        return amount * days_in_month


# main.py
from manager import ExpenseManager
from budget import MonthlyBudget, DailyBudget
from expense import Expense


def get_user_expense():
    print("Getting User Expense")
    name = input("Enter expense name: ")
    amount = float(input("Enter expense amount (₱): "))

    categories = [
        "🍔 Food", "🚌 Transport", "📟 Bills", "🏥 Health",
        "💅 Personal Care", "🎓 Education", "🎮 Entertainment",
        "🎁 Gifts", "🛍️ Shopping", "✈️ Travel", "💸 Debt", "💰 Savings"
    ]

    for i, category in enumerate(categories):
        print(f"  {i + 1}. {category}")

    while True:
        try:
            choice = int(input(f"Enter category number [1 - {len(categories)}]: ")) - 1
            if 0 <= choice < len(categories):
                return Expense(name, amount, categories[choice])
            else:
                print("Invalid category. Try again.")
        except ValueError:
            print("Enter a valid number.")


def main():
    print("Running Expense Tracker!")
    file_path = "expenses.csv"
    manager = ExpenseManager(file_path)

    if input("Do you want to reset all expenses? (y/n): ").lower() == "y":
        manager.reset()

    while True:
        allowance_type = input("Enter (1) Monthly or (2) Daily allowance: ")
        if allowance_type in ["1", "2"]:
            break
        print("Invalid choice. Try again.")

    while True:
        try:
            amount = float(input("Enter your allowance in pesos: ₱"))
            break
        except ValueError:
            print("Invalid amount.")

    strategy = MonthlyBudget() if allowance_type == "1" else DailyBudget()
    budget = strategy.calculate_budget(amount)
    print(f"Your monthly budget is set to: ₱{budget:.2f}\n")

    expense = get_user_expense()
    manager.save_expense(expense)
    manager.load_expenses()
    manager.summarize(budget)


if __name__ == "__main__":
    main()