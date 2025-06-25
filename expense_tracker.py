import calendar
import datetime
from expense import Expense
from budget import BudgetPlanner 

class ExpenseManager:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save_expense(self, expense_data: Expense) -> None:
        print(f"Saving Expense: {expense_data} to {self.file_path}")
        with open(self.file_path, "a", encoding="utf-8") as file:
            file.write(f"{expense_data.name},{expense_data.amount},{expense_data.category}\n")

    def reset_expenses(self) -> None:
        with open(self.file_path, "w") as file:
            pass  # Overwrites the file, making it empty
        print("✅ All expenses have been reset.\n")

class UserInputHandler:
    def __init__(self):
        self.expense_categories = [
            "🍔 Food", "🚌 Transport", "🧾 Bills", "🏥 Health",
            "💅 Personal Care", "🎓 Education", "🎮 Entertainment",
            "🎁 Gifts", "🛍️ Shopping", "✈️ Travel", "💸 Debt", "💰 Savings"
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
    expense_manager = ExpenseManager(file_path)

    reset = input("Do you want to reset all previous expenses? (y/n): ").lower()
    if reset == "y":
        expense_manager.reset_expenses()

    user_input_handler = UserInputHandler()
    user_expense = user_input_handler.get_expense_from_user()

    budget_planner = BudgetPlanner()
    monthly_budget = budget_planner.get_monthly_budget()

    expense_manager.save_expense(user_expense)

    print(f"Remaining budget after 1 expense: ₱{monthly_budget - user_expense.amount:.2f}")


if __name__ == "__main__":
    main()