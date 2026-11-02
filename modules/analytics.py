
import pandas as pd
import numpy as np


class FinancialAnalytics:

    def __init__(self, transactions):
        self.transactions = transactions
        self.df = self.create_dataframe()

    def create_dataframe(self):
        records = [t.to_dict() for t in self.transactions]

        columns = ["id", "title", "amount", "category", "type", "date"]

        df = pd.DataFrame(records, columns=columns)

        if not df.empty:
            df["amount"] = pd.to_numeric(
                df["amount"], errors="coerce"
            )

            df["amount"] = df["amount"].fillna(
                df["amount"].median()
            )

        return df

    def get_summary(self):
        if self.df.empty:
            return {
                "income": 0,
                "expenses": 0,
                "balance": 0,
                "average_expense": 0
            }

        income = self.df.loc[
            self.df["type"] == "Income", "amount"
        ].sum()

        expenses = self.df.loc[
            self.df["type"] == "Expense", "amount"
        ].sum()

        expense_values = self.df.loc[
            self.df["type"] == "Expense", "amount"
        ]

        average_expense = (
            expense_values.mean() if not expense_values.empty else 0
        )

        return {
            "income": float(income),
            "expenses": float(expenses),
            "balance": float(income - expenses),
            "average_expense": float(average_expense)
        }

    def get_category_expenses(self):
        expenses = self.df[
            self.df["type"] == "Expense"
        ]

        return expenses.groupby("category")["amount"].sum()

    def get_monthly_summary(self):
        if self.df.empty:
            return pd.DataFrame(
                columns=["Income", "Expense"]
            )

        df = self.df.copy()
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])

        df["month"] = df["date"].dt.strftime("%Y-%m")

        return df.pivot_table(
            index="month",
            columns="type",
            values="amount",
            aggfunc="sum",
            fill_value=0
        ).reindex(columns=["Income", "Expense"], fill_value=0)

    def get_highest_expense_category(self):
        category_data = self.get_category_expenses()

        if category_data.empty:
            return "No expenses yet"

        return category_data.idxmax()

    def get_numpy_statistics(self):
        amounts = self.df["amount"].dropna().to_numpy()

        if len(amounts) == 0:
            return {
                "maximum": 0,
                "minimum": 0,
                "standard_deviation": 0
            }

        return {
            "maximum": float(np.max(amounts)),
            "minimum": float(np.min(amounts)),
            "standard_deviation": float(np.std(amounts))
        }
