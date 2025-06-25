import calendar
import datetime
from expense import Expense

class Budget:
    def __init__(self, allowance: float, is_daily: bool):
        self.allowance = allowance
        self.is_daily = is_daily
        self.current_date = datetime.datetime.now()
        self.total_days = calendar.monthrange(self.current_date.year, self.current_date.month)[1]
        self.remaining_days = self.total_days - self.current_date.day

    def get_monthly_budget(self):
        return self.allowance * self.total_days if self.is_daily else self.allowance
    
    def get_remaining_days(self):
        return self.remaining_days
    
    def calculate_daily_budget(self, remaining_budget)
        if self.remaining_days > 0:
            return remaining_budget / self.remaining_days
        return 0.0

class UserInputHandler:
    def __init__(self):
        self.expense_categories = [
            "🍔 Food",
        "🚌 Transport",
        "🧾 Bills",
        "🏥 Health",
        "💅 Personal Care",
        "🎓 Education",
        "🎮 Entertainment",
        "🎁 Gifts",
        "🛍️ Shopping",
        "✈️ Travel",
        "💸 Debt",
        "💰 Savings"
        ]

    def get_expense_from_user(self) -> Expense:
        print("Getting User Expense")
        expense_name = input("Enter expense name: ")

        while True:
            try:
                expense_amount = float(input("Enter expense amount (₱): "))
                break
            except ValueError:
                print("Please enter a valid number.")

        while True:
            print("Select a category:")
            for index, category in enumerate(self.expense_categories):
                print(f"  {index + 1}. {category}")

            try:
                selected_index = int(input(f"Enter a category number [1 - {len(self.expense_categories)}]: ")) - 1
                if 0 <= selected_index < len(self.expense_categories):
                    selected_category = self.expense_categories[selected_index]
                    break
                else:
                    print("Invalid category. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

        return Expense(name=expense_name, amount=expense_amount, category=selected_category)


def save_expense_to_file(expense_data: Expense, file_path: str):
    print(f"Saving Expense: {expense_data} to {file_path}")
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(f"{expense_data.name},{expense_data.amount},{expense_data.category}\n")


def summarize_expenses(file_path: str, budget: float):
    print("Summarizing Expenses")
    expenses: list[Expense] = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                name, amount, category = line.strip().split(",")
                loaded_expense = Expense(name=name, amount=float(amount), category=category)
                expenses.append(loaded_expense)
    except FileNotFoundError:
        print("No expense file found yet.")
        return
    except Exception as error:
        print(f"Error reading file: {error}")
        return

    expenses_by_category = {}
    for expense_item in expenses:
        if expense_item.category in expenses_by_category:
            expenses_by_category[expense_item.category] += expense_item.amount
        else:
            expenses_by_category[expense_item.category] = expense_item.amount

    print("Expenses By Category:")
    for category, total_amount in expenses_by_category.items():
        print(f"  {category}: ₱{total_amount:.2f}")

    total_spent = sum(expense.amount for expense in expenses)
    print(f"Total Spent: ₱{total_spent:.2f}")

    remaining_budget = budget - total_spent
    print(f"Budget Remaining: ₱{remaining_budget:.2f}")

    current_date = datetime.datetime.now()
    total_days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
    days_remaining = total_days_in_month - current_date.day

    if days_remaining > 0:
        daily_budget = remaining_budget / days_remaining
        print(f"Budget Per Day: ₱{daily_budget:.2f}")
    else:
        print("Month is ending today. Plan next month's budget!")


if __name__ == "__main__":
    main()