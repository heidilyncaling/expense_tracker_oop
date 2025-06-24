from expense import Expense
import calendar
import datetime


def main():
    print("Running Expense Tracker!")
    expense_file_path = "expenses.csv"

    while True:
        print("Do you want to enter a (1) Monthly or (2) Daily allowance?")
        allowance_type = input("Enter 1 for monthly, 2 for daily: ")
        if allowance_type in ["1", "2"]:
            break
        print("Invalid choice. Please try again.")

    while True:
        try:
            user_allowance = float(input("Enter your allowance in pesos: ₱"))
            break
        except ValueError:
            print("Please enter a valid number.")

    current_date = datetime.datetime.now()
    total_days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]

    if allowance_type == "2":
        monthly_budget = user_allowance * total_days_in_month
    else:
        monthly_budget = user_allowance

    print(f"Your monthly budget is set to: ₱{monthly_budget:.2f}")

    user_expense = get_user_expense()
    save_expense_to_file(user_expense, expense_file_path)
    summarize_expenses(expense_file_path, monthly_budget)


def get_user_expense():
    print("Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount (₱): "))

    expense_categories = [
        "Food",
        "Transport",
        "Bills",
        "Health",
        "Personal Care",
        "Education",
        "Entertainment",
        "Gifts",
        "Shopping",
        "Travel",
        "Debt",
        "Savings"
    ]

    while True:
        print("Select a category:")
        for index, category in enumerate(expense_categories):
            print(f"  {index + 1}. {category}")

        category_range = f"[1 - {len(expense_categories)}]"
        try:
            selected_category_index = int(input(f"Enter a category number {category_range}: ")) - 1
            if 0 <= selected_category_index < len(expense_categories):
                selected_category = expense_categories[selected_category_index]
                return Expense(name=expense_name, category=selected_category, amount=expense_amount)
            else:
                print("Invalid category. Please try again!")
        except ValueError:
            print("Please enter a valid number.")


def save_expense_to_file(expense_data: Expense, file_path: str):
    print(f"Saving Expense: {expense_data} to {file_path}")
    with open(file_path, "a") as file:
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