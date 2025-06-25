import calendar
import datetime
from expense import Expense
from budget import Budget

class ExpenseManager:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save_expense(self, expense_data: Expense) -> None:
        print(f"Saving Expense: {expense_data} to {self.file_path}")
        with open(self.file_path, "a", encoding="utf-8") as file:
            file.write(f"{expense_data.name},{expense_data.amount},{expense_data.category}\n")

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
    
    def calculate_daily_budget(self, remaining_budget):
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

def main():
    file_path = "expenses.csv"

    user_input_handler = UserInputHandler()
    user_expense = user_input_handler.get_expense_from_user()

    allowance = float(input("Enter your allowance (₱): "))
    is_daily = input("Is this a daily allowance? (y/n): ").lower() == "y"

    budget = Budget(allowance, is_daily)

    expense_manager = ExpenseManager(file_path)
    expense_manager.save_expense(user_expense)

if __name__ == "__main__":
    main()