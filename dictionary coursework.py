import json
import datetime

transactions = {}


def load_transactions():
    try:
        with open("coursework.json", "r") as file:
            transactions = json.load(file)
            return transactions
    except FileNotFoundError:
        print("File not found.")
    except json.decoder.JSONDecodeError:
        print(f"The file '{filename}' is empty or contains invalid JSON.")
    else:
        print(transactions)

    return {}


def save_transactions():
    with open("coursework.json", "w") as file:
        json.dump(transactions, file)

def read_bulk_transactions_from_file(filename):
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

        save_transactions()  # Save the updated transactions to the JSON file
        print("Bulk transactions read successfully!")

    except FileNotFoundError:
        print("File not found.")



def add_transaction():
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
    for category, expenses in transactions.items():
        print(f"{category}:")
        for expense in expenses:
            print(f"  Amount: {expense['amount']}, Date: {expense['date']}")

def update_transaction():
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

                transaction_to_update = list(transactions.values())[index][0]
                transaction_to_update["amount"] = amount
                transaction_to_update["date"] = date
                transaction_to_update["category"] = category

                print("Transaction updated successfully!")
                break
            else:
                print("Invalid index. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    save_transactions()


def delete_transaction():
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
    if not transactions:
        print("No transactions found.")
        return

    print("Summary of Transactions:")
    for category, expenses in transactions.items():
        total_amount = sum(expense['amount'] for expense in expenses)
        print(f"{category}: Total amount = {total_amount}")


def main_menu():
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
