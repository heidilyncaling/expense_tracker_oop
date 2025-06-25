import calendar
import datetime
from abc import ABC, abstractmethod
from expense import Expense


# ABSTRACT BASE CLASS (Abstraction)
class SummaryBase(ABC):
    @abstractmethod
    def display_summary(self, file_path: str, budget: float) -> None:
        pass


# CHILD CLASS (Inheritance + Polymorphism)
class ExpenseSummary(SummaryBase):
    def display_summary(self, file_path: str, budget: float) -> None:
        expenses: list[Expense] = []

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    name, amount, category = line.strip().split(",")
                    expense = Expense(name=name, amount=float(amount), category=category)
                    expenses.append(expense)
        except FileNotFoundError:
            print("No expense file found yet.")
            return
        except Exception as error:
            print(f"Error reading file: {error}")
            return

        expenses_by_category = {}
        for expense in expenses:
            if expense.category in expenses_by_category:
                expenses_by_category[expense.category] += expense.amount
            else:
                expenses_by_category[expense.category] = expense.amount

        print("\n Expenses By Category:")
        for category, total_amount in expenses_by_category.items():
            print(f"  {category}: ₱{total_amount:.2f}")

        total_spent = sum(exp.amount for exp in expenses)
        remaining_budget = budget - total_spent

        print(f"\nTotal Spent: ₱{total_spent:.2f}")
        print(f"Budget Remaining: ₱{remaining_budget:.2f}")

        current_date = datetime.datetime.now()
        total_days = calendar.monthrange(current_date.year, current_date.month)[1]
        days_remaining = total_days - current_date.day

        if days_remaining > 0:
            daily_budget = remaining_budget / days_remaining
            print(f"Daily Budget Left: ₱{daily_budget:.2f}")
        else:
            print(" Month is ending today. Time to plan for next month!")