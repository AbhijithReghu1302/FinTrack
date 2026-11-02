
from modules.transaction import Transaction
from modules.budget import Budget
from modules.storage import DataStorage
from modules.analytics import FinancialAnalytics


# Creating sample transactions
transactions = [
    Transaction("Monthly Allowance", 15000, "Allowance", "Income"),
    Transaction("Food", 2500, "Food", "Expense"),
    Transaction("Shopping", 3000, "Shopping", "Expense"),
    Transaction("Freelance Work", 5000, "Freelance", "Income"),
    Transaction("Transport", 1000, "Transport", "Expense")
]

budgets = [
    Budget("Food", 5000, 11, 2026),
    Budget("Shopping", 4000, 11, 2026)
]


# Testing JSON storage
storage = DataStorage()
storage.save_data(transactions, budgets)

print("DATA SAVED SUCCESSFULLY!")


# Loading saved data
loaded_transactions = storage.load_transactions()
loaded_budgets = storage.load_budgets()

print("Transactions Loaded:", len(loaded_transactions))
print("Budgets Loaded:", len(loaded_budgets))


# Financial analytics
analytics = FinancialAnalytics(loaded_transactions)

print("\nFINANCIAL SUMMARY")
print(analytics.get_summary())

print("\nCATEGORY-WISE EXPENSES")
print(analytics.get_category_expenses())

print("\nHIGHEST EXPENSE CATEGORY")
print(analytics.get_highest_expense_category())

print("\nNUMPY STATISTICS")
print(analytics.get_numpy_statistics())

print("\nMONTHLY SUMMARY")
print(analytics.get_monthly_summary())
