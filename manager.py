from expense import Expense
import calendar
import datetime

class ExpenseManager:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def reset_expenses(self):
        with open(self.file_path, "w") as file:
            pass
        print("All expenses have been reset.\n")

        def save_expenses(self, expense_data: Expense):
            print(f"Saving Expense: {expense_data} to {self.file_path}")
            with open(self.file_path, "a", encoding="utf-8") as file:
                file.write(f"{expense_data.name},{expense_data.amount},{expense_data.category}\n")

        def summarize_expenses(self, budget: float):
            print("Summarizing expenses")
            expenses: list[Expense] = []

            try:
                with open(self.file_path, "r", encoding="utf-8") as file:
                    lines = file.readines()
                    for line in lines:
                        name, amount, category = line.strip().split(",")
                        loaded_expense = Expense(name=name, amount=float(amount), category=category)
                        expenses.apppend(loaded_expense) 
            except FileNotFoundError:
                print("No expense file found yet.")
                return
            except Exception as error:
                print(f"Error reading file: {error}")
                return
            
                           
                           


