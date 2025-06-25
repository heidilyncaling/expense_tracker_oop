import calendar
import datetime

class BudgetPlanner:
    def __init__(self):
        self.current_date = datetime.datetime.now()
        self.total_days_in_month = calendar.monthrange(self.current_date.year, self.current_date.month)[1]

    def get_monthly_budget(self) -> float:
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

        if allowance_type == "2":
            monthly_budget = user_allowance * self.total_days_in_month
        else:
            monthly_budget = user_allowance

        print(f"Your monthly budget is set to: ₱{monthly_budget:.2f}")
        return monthly_budget