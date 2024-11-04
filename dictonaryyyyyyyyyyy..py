import json
import datetime
import tkinter as tk
from tkinter import ttk

transactions = {}  # Dictionary to store transactions

def load_transactions():
    """Load transactions from a JSON file."""
    try:
        with open("coursework.json", "r") as file:
            transactions = json.load(file)
            return transactions
    except FileNotFoundError:
        print("File not found.")
    except json.decoder.JSONDecodeError:
        print("The file is empty or contains invalid JSON.")
    return {}

def save_transactions():
    """Save transactions to a JSON file."""
    with open("coursework.json", "w") as file:
        json.dump(transactions, file)

def read_bulk_transactions_from_file(filename):
    """Read bulk transactions from a text file."""
    try:
        file_path = input("Enter the file path: ")

        with open(fr"{file_path}\{filename}.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) != 4:
                    print("Invalid format in line:", line)
                    continue

                key, amount, type_, date = parts

                try:
                    amount = float(amount)
                except ValueError:
                    print("Invalid amount format in line:", line)
                    continue

                transactions.setdefault(key, []).append({
                    "amount": amount,
                    "date": date,
                    "type": type_
                })

        save_transactions()
        print("Bulk transactions read successfully!")

    except FileNotFoundError:
        print("File not found.")

def add_transaction():
    """Add a transaction manually."""
    category = None
    while True:
        category = input("Enter category: ")
        if category and not category.isdigit():
            break
        else:
            print("Invalid category. Please try again.")

    amount = None
    while True:
        amount_str = input("Enter the amount: ")
        try:
            amount = float(amount_str)
            break
        except ValueError:
            print("Invalid entry. Please enter a valid number.")

    while True:
        date_str = input("Enter the date (YYYY-MM-DD): ")
        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            break
        except ValueError:
            print("Invalid date format. Please try again.")

    transaction = {"amount": amount, "date": str(date)}
    if category not in transactions:
        transactions[category] = []

    transactions[category].append(transaction)

    print("Transaction added successfully!")
    save_transactions()

def view_transactions():
    """View transactions using a GUI."""
    if not transactions:
        print("no transactions to display")
    else:
        # Define the GUI class for transaction viewing
        class FinanceTrackerGUI:
            def __init__(self, root):
                # Initialize GUI
                self.root = root
                self.root.title("Personal Finance Tracker")
                self.create_widgets()
                self.file_name = "coursework.json"  # File name only, assuming it's in the same directory as the script
                self.transactions = self.load_transactions()

            def create_widgets(self):
                # Create GUI widgets
                # (Omitted for brevity)

            def add_transaction(self):
                # Add transaction logic
                # (Omitted for brevity)

            def display_transactions(self):
                # Display transactions logic
                # (Omitted for brevity)

            def load_transactions(self):
                # Load transactions logic
                # (Omitted for brevity)

            def save_transactions(self):
                # Save transactions logic
                # (Omitted for brevity)

            def search_transactions(self):
                # Search transactions logic
                # (Omitted for brevity)

            def sort_by_column(self, col):
                # Sort transactions by column logic
                # (Omitted for brevity)

        def main():
            # Main function for GUI initialization and event loop
            # (Omitted for brevity)

        if __name__ == "__main__":
            main()

def update_transaction():
    """Update a transaction."""
    view_transactions()
    if not transactions:
        return

    while True:
        try:
            index = int(input("Enter index of transaction to update: ")) - 1
            if 0 <= index < len(transactions):
                category = input("Enter new category:  ")
                amount = float(input("Enter new amount: "))
                date = input("Enter new date: (YYYY-MM-DD): ")

                # Update transaction details
                transaction_to_update = list(transactions.values())[index][0]
                transaction_to_update["amount"] = amount
                transaction_to_update["date"] = date

                # Update category in the transactions dictionary
                old_category = list(transactions.keys())[index]
                transactions[category] = transactions.pop(old_category)

                print("Transaction updated successfully!")
                break
            else:
                print("Invalid index. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    save_transactions()

def delete_transaction():
    """Delete a transaction."""
    view_transactions()
    if not transactions:
        print("No transactions found.")
        return

    category = input("Enter category of transaction to delete: ")
    index = int(input("Enter index of transaction to delete: ")) - 1

    if category in transactions and 0 <= index < len(transactions[category]):
        del transactions[category][index]
        print("Transaction deleted successfully!")
        save_transactions()
    else:
        print("Invalid category or index. Please try again.")

def display_summary():
    """Display summary of transactions."""
    if not transactions:
        print("No transactions found.")
        return

    print("Summary of Transactions:")
    for category, expenses in transactions.items():
        total_amount = sum(expense['amount'] for expense in expenses)
        print(f"{category}: Total amount = {total_amount}")

def main_menu():
    """Main menu for user interaction."""
    load_transactions()

    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Read Bulk Transactions from File")
        print("7. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            update_transaction()
        elif choice == "4":
            delete_transaction()
        elif choice == "5":
            display_summary()
        elif choice == "6":
            filename = input("Enter the filename: ")
            read_bulk_transactions_from_file(filename)
        elif choice == "7":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
