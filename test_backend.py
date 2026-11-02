from modules.user import User
from modules.transaction import Transaction
from modules.budget import Budget
from modules.utilities import (
    find_twin_primes,
    permutation,
    combination
)

# Creating a user
user = User(101, "Alex", 21)
print("USER DETAILS:", user.display_details())

# Creating transactions
income = Transaction(
    "Monthly Allowance", 15000, "Allowance", "Income"
)

expense = Transaction(
    "Food", 2500, "Food", "Expense"
)

print("\nINCOME:", income.to_dict())
print("EXPENSE:", expense.to_dict())

# Creating a budget
budget = Budget("Food", 5000, 11, 2026)

spent = expense.amount

print("\nBUDGET DETAILS")
print("Remaining:", budget.remaining_budget(spent))
print("Usage:", budget.usage_percentage(spent), "%")

# Mathematical utilities
print("\nTWIN PRIMES:", find_twin_primes(100))

print("PERMUTATION:", permutation(5, 2))
print("COMBINATION:", combination(5, 2))