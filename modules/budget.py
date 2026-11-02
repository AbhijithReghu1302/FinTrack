class Budget:
    def __init__(self, category, limit_amount, month, year):
        if limit_amount <= 0:
            raise ValueError("Budget must be greater than zero.")

        self.category = category
        self.limit_amount = float(limit_amount)
        self.month = month
        self.year = year

    def remaining_budget(self, spent):
        return self.limit_amount - spent

    def usage_percentage(self, spent):
        return (spent / self.limit_amount) * 100

    def to_dict(self):
        return {
            "category": self.category,
            "limit": self.limit_amount,
            "month": self.month,
            "year": self.year
        }