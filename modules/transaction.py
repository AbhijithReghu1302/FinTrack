from datetime import date
import uuid


class Transaction:
    def __init__(self, title, amount, category, transaction_type,
                 transaction_date=None):

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        if transaction_type not in ["Income", "Expense"]:
            raise ValueError("Type must be Income or Expense.")

        self.transaction_id = str(uuid.uuid4())[:8]
        self.title = title
        self.amount = float(amount)
        self.category = category
        self.transaction_type = transaction_type
        self.transaction_date = transaction_date or date.today().isoformat()

    def to_dict(self):
        return {
            "id": self.transaction_id,
            "title": self.title,
            "amount": self.amount,
            "category": self.category,
            "type": self.transaction_type,
            "date": self.transaction_date
        }

    @classmethod
    def from_dict(cls, data):
        transaction = cls(
            data["title"],
            data["amount"],
            data["category"],
            data["type"],
            data["date"]
        )
        transaction.transaction_id = data["id"]
        return transaction