class Expense:
    def __init__(self, name: str, category: str, amount: float) -> None:
        self.name = name
        self.category = category
        self.amount = amount

    def __repr__(self):
        return f"<Expense: {self.name}, {self.category}, ₱{self.amount:.2f}>"