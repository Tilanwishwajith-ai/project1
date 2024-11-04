import json
import datetime
import tkinter as tk
from tkinter import ttk


transactions = {}# Dictionary to store transactions


# load transaction json file
def load_transactions():
    try:
        with open("coursework.json", "r") as file:
            transactions = json.load(file)
            return transactions
    except FileNotFoundError:
        print("File not found.")
    except json.decoder.JSONDecodeError:
        print("The file is empty or contains invalid JSON.")
    else:
        print(transactions)
    return {}


# save transaction json file
def save_transactions():
    with open("coursework.json", "w") as file:
        json.dump(transactions, file)

# read transaction to read bulk text file
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

        save_transactions()
        print("Bulk transactions read successfully!")

    except FileNotFoundError:
        print("File not found.")

# add transaction
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


#"View transactions using a GUI.""
def view_transactions():
    if not transactions:
        print("no transactions to display")
    else:
        # define the GUI class for transaction viewing
        class FinanceTrackerGUI:
            def __init__(self, root):
                self.root = root
                self.root.title("Personal Finance Tracker")
                self.create_widgets()
                self.file_name = "coursework.json"  # File name only, assuming it's in the same directory as the script
                self.transactions = self.load_transactions()

            # Create GUI widgets
            def create_widgets(self):
                # Frame for table and scrollbar
                self.frame = ttk.Frame(self.root)
                self.frame.pack(fill='both', expand=True,padx=20, pady=50)

                # Treeview for displaying transactions
                self.my_tree = ttk.Treeview(self.frame, columns=("category", "amount", "date"), show="headings")
                self.my_tree.column("category", anchor='w', width=120)  # 'w' for west (left-aligned)
                self.my_tree.column("amount", anchor='center', width=80)  # 'center' for center-aligned
                self.my_tree.column("date", anchor='w', width=120)  # 'w' for west (left-aligned)

                # Create headings
                self.my_tree.heading("category", text="Category", anchor='w',
                                     command=lambda: self.sort_by_column("category"))
                self.my_tree.heading("amount", text="Amount", anchor='center',
                                     command=lambda: self.sort_by_column("amount"))
                self.my_tree.heading("date", text="Date", anchor='w', command=lambda: self.sort_by_column("date"))

                # Add scrollbar
                scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.my_tree.yview)
                scrollbar.grid(row=0, column=1, sticky='ns')
                self.my_tree.configure(yscrollcommand=scrollbar.set)

                self.my_tree.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

                # Frame for entry widgets
                entry_frame = ttk.Frame(self.root)
                entry_frame.pack(fill='x')

                # Entry widgets for adding transactions
                self.category_entry = ttk.Entry(entry_frame)
                self.category_entry.grid(row=0, column=0, padx=5, pady=5)
                ttk.Label(entry_frame, text="Category:").grid(row=0, column=1, padx=5, pady=5)

                self.amount_entry = ttk.Entry(entry_frame)
                self.amount_entry.grid(row=1, column=0, padx=5, pady=5)
                ttk.Label(entry_frame, text="Amount:").grid(row=1, column=1, padx=5, pady=5)

                self.date_entry = ttk.Entry(entry_frame)
                self.date_entry.grid(row=2, column=0, padx=5, pady=5)
                ttk.Label(entry_frame, text="Date (YYYY-MM-DD):").grid(row=2, column=1, padx=5, pady=5)

                ttk.Button(entry_frame, text="Add Transaction", command=self.add_transaction).grid(row=3, columnspan=2,
                                                                                                   padx=5, pady=5)

                # Search bar entry and button
                self.search_entry = ttk.Entry(entry_frame)
                self.search_entry.grid(row=4, column=0, padx=5, pady=5)
                ttk.Button(entry_frame, text="Search", command=self.search_transactions).grid(row=4, column=1, padx=5,
                                                                                              pady=5)

            # Add transaction logic
            def add_transaction(self):
                category = self.category_entry.get()
                amount_str = self.amount_entry.get()
                date_str = self.date_entry.get()

                if not category or category.isdigit():
                    print("Invalid category. Please try again.")
                    return

                try:
                    amount = float(amount_str)
                except ValueError:
                    print("Invalid amount. Please enter a valid number.")
                    return

                try:
                    date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    print("Invalid date format. Please try again.")
                    return

                transaction = {"amount": amount, "date": str(date)}
                if category not in self.transactions:
                    self.transactions[category] = []

                self.transactions[category].append(transaction)

                print("Transaction added successfully!")
                self.save_transactions()
                self.display_transactions()

            # Display transactions logic
            def display_transactions(self):
                # Clear existing items in the treeview
                for item in self.my_tree.get_children():
                    self.my_tree.delete(item)


                for category, transactions in self.transactions.items():
                    for transaction in transactions:
                        self.my_tree.insert("", "end", values=(category, transaction["amount"], transaction["date"]))


            #gui table to json file load
            def load_transactions(self):
                try:
                    with open("coursework.json", "r") as file:
                        transactions = json.load(file)
                        return transactions
                except FileNotFoundError:
                    print("File not found.")
                except json.decoder.JSONDecodeError:
                    print(f"The file '{self.file_name}' is empty or contains invalid JSON.")
                return {}

            #save file
            def save_transactions(self):
                with open("coursework.json", "w") as file:
                    json.dump(self.transactions, file)

            # search transaction(search bar)
            def search_transactions(self):
                category = self.search_entry.get().lower()

                # Clear existing items in the treeview
                self.display_transactions()


                if category in self.transactions:
                    self.my_tree.delete(*self.my_tree.get_children())
                    for transaction in self.transactions[category]:
                        self.my_tree.insert("", "end", values=(category, transaction["amount"], transaction["date"]))

            # Sort transactions by column logic
            def sort_by_column(self, col):
                data = [(self.my_tree.set(child, col), child) for child in self.my_tree.get_children('')]
                data.sort(reverse=False)

                for index, (val, child) in enumerate(data):
                    self.my_tree.move(child, '', index)


                self.my_tree.heading(col, command=lambda: self.sort_by_column(col))

        def main():
            root = tk.Tk()
            root.geometry("600x600")
            app = FinanceTrackerGUI(root)
            app.display_transactions()  # Display transactions initially
            root.mainloop()

        if __name__ == "__main__":
            main()

# update transaction
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

                # Get the transaction to update
                transaction_to_update = list(transactions.values())[index][0]

                # Update the transaction details
                transaction_to_update["amount"] = amount
                transaction_to_update["date"] = date

                # Update the category in the transactions dictionary
                old_category = list(transactions.keys())[index]
                transactions[category] = transactions.pop(old_category)

                print("Transaction updated successfully!")
                break
            else:
                print("Invalid index. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    save_transactions()
# delete transaction
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


# display of summary of transaction
def display_summary():
    if not transactions:
        print("No transactions found.")
        return

    print("Summary of Transactions:")
    for category, expenses in transactions.items():
        total_amount = sum(expense['amount'] for expense in expenses)
        print(f"{category}: Total amount = {total_amount}")

# main menu
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
