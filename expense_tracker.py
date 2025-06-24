from expense import Expense
import calendar
import datetime


def main():
    print("Running Expense Tracker!")
    expense_file_path = "expenses.csv"

    # Ask user for budget input
    while True:
        print("Do you want to enter a (1) Monthly or (2) Daily allowance?")
        allowance_choice = input("Enter 1 for monthly, 2 for daily: ")
        if allowance_choice in ["1", "2"]:
            break
        print("Invalid choice. Please try again.")

    while True:
        try:
            allowance_amount = float(input("Enter your allowance in pesos: ₱"))
            break
        except ValueError:
            print("Please enter a valid number.")

    current_date = datetime.datetime.now()
    days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]

    if allowance_choice == "2":
        budget = allowance_amount * days_in_month
    else:
        budget = allowance_amount

    print(f"Your monthly budget is set to: ₱{budget:.2f}")

    # Get user input for expense
    user_expense = get_user_expense()

    # Write the expense to a file
    save_expense_to_file(user_expense, expense_file_path)

    # Read file and summarize expenses
    summarize_expenses(expense_file_path, budget)


def get_user_expense():
    print("Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount (₱): "))

    expense_categories = [
        "Food",
        "Home",
        "Work",
        "Fun",
        "Misc",
    ]

    while True:
        print("Select a category:")
        for index, category_name in enumerate(expense_categories):
            print(f"  {index + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name,
                category=selected_category,
                amount=expense_amount
            )
            return new_expense
        else:
            print("Invalid category. Please try again!")


def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"Saving Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a") as file:
        file.write(f"{expense.name},{expense.amount},{expense.category}\n")


def summarize_expenses(expense_file_path, budget):
    print("Summarizing Expenses")
    expenses: list[Expense] = []

    with open(expense_file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category = line.strip().split(",")
            loaded_expense = Expense(
                name=expense_name,
                amount=float(expense_amount),
                category=expense_category
            )
            expenses.append(loaded_expense)

    amount_by_category = {}
    for expense in expenses:
        category_key = expense.category
        if category_key in amount_by_category:
            amount_by_category[category_key] += expense.amount
        else:
            amount_by_category[category_key] = expense.amount

    print("Expenses By Category:")
    for category, amount in amount_by_category.items():
        print(f"  {category}: ₱{amount:.2f}")

    total_spent = sum(exp.amount for exp in expenses)
    print(f"Total Spent: ₱{total_spent:.2f}")

    remaining_budget = budget - total_spent
    print(f"Budget Remaining: ₱{remaining_budget:.2f}")

    current_date = datetime.datetime.now()
    days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
    remaining_days = days_in_month - current_date.day

    if remaining_days > 0:
        daily_budget = remaining_budget / remaining_days
        print(f"Budget Per Day: ₱{daily_budget:.2f}")
    else:
        print("Month is ending today. Plan next month's budget!")


def green(text):
    return text  # No colored output needed


if __name__ == "__main__":
    main()