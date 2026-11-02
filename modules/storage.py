
import json
from pathlib import Path


class DataStorage:
    def __init__(self):
        self.data_folder = Path(__file__).resolve().parent.parent / "data"
        self.data_folder.mkdir(exist_ok=True)

        self.transaction_file = self.data_folder / "transactions.json"
        self.budget_file = self.data_folder / "budgets.json"

    def save_data(self, transactions, budgets):
        with open(self.transaction_file, "w") as file:
            json.dump(
                [t.to_dict() for t in transactions],
                file,
                indent=4
            )

        with open(self.budget_file, "w") as file:
            json.dump(
                [b.to_dict() for b in budgets],
                file,
                indent=4
            )

    def load_transactions(self):
        from modules.transaction import Transaction

        if not self.transaction_file.exists():
            return []

        with open(self.transaction_file, "r") as file:
            data = json.load(file)

        return [Transaction.from_dict(item) for item in data]

    def load_budgets(self):
        from modules.budget import Budget

        if not self.budget_file.exists():
            return []

        with open(self.budget_file, "r") as file:
            data = json.load(file)

        return [
            Budget(
                item["category"],
                item["limit"],
                item["month"],
                item["year"]
            )
            for item in data
        ]
