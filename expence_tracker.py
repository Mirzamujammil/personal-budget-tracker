import calendar

from expence import Expense
from datetime import datetime


def main():
    expenses_file_path = "expenses.csv"
    budget = 2000

    # get user input for expense
    expense = get_user_expense()
    # write their expense to the file
    save_expense_to_the_file(expense, expenses_file_path)
    # read file and summarize expense
    summarize_expenses(expenses_file_path, budget)


def get_user_expense():
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))

    expense_categories = [
        "🍔 food",
        "🏠 home",
        "💼 work",
        "🎉 fun",
        "🕜 other"
    ]
    while True:
        print("Select a category:")
        for i, category in enumerate(expense_categories):  # Changed variable name from expense_name to category
            print(f"{i + 1}. {category}")

        value_range = f"[1 - {len(expense_categories)}]"
        select_index = int(input(f"Enter a category number {value_range}: ")) - 1

        if select_index in range(len(expense_categories)):
            selected_category = expense_categories[select_index]
            new_expense = Expense(name=expense_name, category=selected_category, amount=expense_amount)
            return new_expense
        else:
            print("Invalid category. Please try again!")


def save_expense_to_the_file(expense: Expense, expenses_file_path):
    print(f"🎯 Saving user expense {expense} to {expenses_file_path}")
    with open(expenses_file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name}, {expense.amount}, {expense.category}\n")


def summarize_expenses(expenses_file_path, budget):
    expenses: list[Expense] = []
    with open(expenses_file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 3:
                expense_name, expense_amount, expense_category = parts
                line_expense = Expense(
                    name=expense_name.strip(),
                    amount=float(expense_amount.strip()),
                    category=expense_category.strip()
                )
                expenses.append(line_expense)

            else:
                print(f"Ignoring line: {line.strip()} - Unexpected format")

    amount_by_categroy = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_categroy:
            amount_by_categroy[key] += expense.amount
        else:
            amount_by_categroy[key] = expense.amount
    print("expenses by category")
    for key, amount in amount_by_categroy.items():
        print(f"{key}: ₹{amount: .2f}")

    total_spent = sum([x.amount for x in expenses])
    print(f"you have spent {total_spent: .2f} this month!")

    remaining_budget = budget - total_spent
    print(f"remaining budget is {remaining_budget: .2f} for this month!")

    # Get the current date
    now = datetime.now()

    # Define the target date
    days_in_month = calendar.monthrange(now.year, now.month)[1]  # Change this to your target date

    # Calculate the difference between the target date and the current date
    remaining_days = days_in_month - now.day

    print(f"Number of remaining days: {remaining_days}")

    daily_budget = remaining_budget / remaining_days
    print(f"budget per day: {daily_budget: .2f}")


if __name__ == "__main__":
    main()
