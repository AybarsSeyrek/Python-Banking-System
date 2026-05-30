# Python Banking System
# This is a terminal-based banking program.
# It includes account numbers, PIN login, multiple accounts,
# deposits, withdrawals, transfers, transaction history,
# transaction filtering, monthly statement export, and JSON saving.

import json
import os
import random
from datetime import datetime


ACCOUNT_FILE = "bank_accounts.json"
BACK_OPTIONS = ["b", "back", "return"]
MAX_LOGIN_ATTEMPTS = 3


def load_accounts():
    # Load all saved accounts from the JSON file.
    # If the file does not exist yet, start with an empty dictionary.
    if not os.path.exists(ACCOUNT_FILE):
        return {}

    try:
        with open(ACCOUNT_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError:
        # If the JSON file is empty or broken, avoid crashing the program.
        return {}


def save_accounts(accounts):
    # Save all account data back into the JSON file.
    with open(ACCOUNT_FILE, "w", encoding="utf-8") as file:
        json.dump(accounts, file, indent=4)


def get_current_time():
    # Returns a readable timestamp for transactions.
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def is_back_choice(user_input):
    # Checks if the user wants to cancel the current action.
    return user_input.lower().strip() in BACK_OPTIONS


def generate_account_number(accounts):
    # Generate a unique 6-digit account number.
    # The while loop makes sure the number is not already used.
    while True:
        account_number = str(random.randint(100000, 999999))

        if account_number not in accounts:
            return account_number


def display_welcome_menu():
    print("=" * 50)
    print("              PYTHON BANKING SYSTEM")
    print("=" * 50)
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")
    print("=" * 50)


def display_banking_menu(account):
    print("\n" + "=" * 50)
    print(f"        BANKING MENU - {account['name']}")
    print(f"        Account Number: {account['account_number']}")
    print("=" * 50)
    print("1. Show Balance")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Transfer Money")
    print("5. View Transaction History")
    print("6. Filter/Search Transactions")
    print("7. Export Monthly Statement")
    print("8. Change PIN")
    print("9. Delete Account")
    print("10. Logout")
    print("=" * 50)


def get_menu_choice(valid_choices):
    # General menu input validator.
    while True:
        choice = input("Enter your choice: ").strip()

        if choice in valid_choices:
            return choice

        print("Invalid choice. Please try again.")


def get_valid_name():
    # Ask for the user's name.
    # The user can type b/back/return to cancel.
    while True:
        name = input("Enter account holder name (or type 'b' to go back): ").strip()

        if is_back_choice(name):
            return None

        if name:
            return name

        print("Name cannot be empty.")


def get_valid_pin(message="Create a 4-digit PIN"):
    # PIN must be exactly 4 digits.
    # This is simple authentication for the project.
    while True:
        pin = input(f"{message} (or type 'b' to go back): ").strip()

        if is_back_choice(pin):
            return None

        if pin.isdigit() and len(pin) == 4:
            return pin

        print("Invalid PIN. PIN must be exactly 4 digits.")


def get_valid_amount(message):
    # Ask for a money amount.
    # This prevents crashes if the user types letters.
    while True:
        amount_text = input(f"{message} (or type 'b' to go back): ").strip()

        if is_back_choice(amount_text):
            return None

        try:
            amount = float(amount_text)

            if amount > 0:
                return round(amount, 2)

            print("Amount must be greater than 0.")

        except ValueError:
            print("Invalid amount. Please enter a valid number.")


def add_transaction(account, transaction_type, amount, balance_after, note=""):
    # Store each transaction as a dictionary.
    # This makes transaction history easier to filter and export.
    transaction = {
        "type": transaction_type,
        "amount": round(amount, 2),
        "balance_after": round(balance_after, 2),
        "note": note,
        "date_time": get_current_time()
    }

    account["transactions"].append(transaction)


def create_account(accounts):
    print("\nCreate New Account")
    print("-" * 50)

    name = get_valid_name()

    if name is None:
        print("Account creation cancelled.")
        return

    pin = get_valid_pin()

    if pin is None:
        print("Account creation cancelled.")
        return

    account_number = generate_account_number(accounts)

    # Better account data structure:
    # The account number is the unique key.
    # The account holder name is stored inside the account data.
    accounts[account_number] = {
        "account_number": account_number,
        "name": name,
        "pin": pin,
        "balance": 0.0,
        "status": "active",
        "transactions": []
    }

    save_accounts(accounts)

    print("\nAccount created successfully!")
    print(f"Account Holder: {name}")
    print(f"Account Number: {account_number}")
    print("Please save your account number. You need it to log in.")


def login(accounts):
    print("\nLogin")
    print("-" * 50)

    account_number = input("Enter account number (or type 'b' to go back): ").strip()

    if is_back_choice(account_number):
        print("Login cancelled.")
        return None

    if account_number not in accounts:
        print("Account not found.")
        return None

    account = accounts[account_number]

    # Login attempt limit.
    # If the user enters the wrong PIN 3 times, they return to the main menu.
    attempts = 0

    while attempts < MAX_LOGIN_ATTEMPTS:
        pin = get_valid_pin("Enter your 4-digit PIN")

        if pin is None:
            print("Login cancelled.")
            return None

        if pin == account["pin"]:
            print(f"\nLogin successful. Welcome back, {account['name']}!")
            return account_number

        attempts += 1
        attempts_left = MAX_LOGIN_ATTEMPTS - attempts
        print(f"Incorrect PIN. Attempts left: {attempts_left}")

    print("Too many failed attempts. Returning to main menu.")
    return None


def show_balance(account):
    print("\n" + "*" * 50)
    print(f"Account Holder: {account['name']}")
    print(f"Account Number: {account['account_number']}")
    print(f"Current Balance: ${account['balance']:.2f}")
    print("*" * 50)


def print_receipt(transaction_type, amount, balance):
    # A receipt gives the user confirmation after a transaction.
    print("\n" + "=" * 50)
    print("              TRANSACTION RECEIPT")
    print("=" * 50)
    print(f"Type: {transaction_type}")
    print(f"Amount: ${amount:.2f}")
    print(f"New Balance: ${balance:.2f}")
    print(f"Date/Time: {get_current_time()}")
    print("=" * 50)


def deposit_money(accounts, account_number):
    account = accounts[account_number]

    print("\nDeposit Money")
    print("-" * 50)

    amount = get_valid_amount("Enter amount to deposit")

    if amount is None:
        print("Deposit cancelled.")
        return

    account["balance"] += amount

    add_transaction(
        account,
        "Deposit",
        amount,
        account["balance"],
        "Money deposited into account"
    )

    save_accounts(accounts)

    print("Deposit successful!")
    print_receipt("Deposit", amount, account["balance"])


def withdraw_money(accounts, account_number):
    account = accounts[account_number]

    print("\nWithdraw Money")
    print("-" * 50)

    amount = get_valid_amount("Enter amount to withdraw")

    if amount is None:
        print("Withdrawal cancelled.")
        return

    if amount > account["balance"]:
        print("Insufficient funds.")
        return

    account["balance"] -= amount

    add_transaction(
        account,
        "Withdrawal",
        amount,
        account["balance"],
        "Money withdrawn from account"
    )

    save_accounts(accounts)

    print("Withdrawal successful!")
    print_receipt("Withdrawal", amount, account["balance"])


def transfer_money(accounts, sender_account_number):
    sender_account = accounts[sender_account_number]

    print("\nTransfer Money")
    print("-" * 50)

    receiver_account_number = input("Enter receiver account number (or type 'b' to go back): ").strip()

    if is_back_choice(receiver_account_number):
        print("Transfer cancelled.")
        return

    if receiver_account_number not in accounts:
        print("Receiver account not found.")
        return

    if receiver_account_number == sender_account_number:
        print("You cannot transfer money to your own account.")
        return

    amount = get_valid_amount("Enter amount to transfer")

    if amount is None:
        print("Transfer cancelled.")
        return

    if amount > sender_account["balance"]:
        print("Insufficient funds.")
        return

    receiver_account = accounts[receiver_account_number]

    sender_account["balance"] -= amount
    receiver_account["balance"] += amount

    add_transaction(
        sender_account,
        "Transfer Sent",
        amount,
        sender_account["balance"],
        f"Transferred to account {receiver_account_number}"
    )

    add_transaction(
        receiver_account,
        "Transfer Received",
        amount,
        receiver_account["balance"],
        f"Received from account {sender_account_number}"
    )

    save_accounts(accounts)

    print("Transfer successful!")
    print_receipt("Transfer Sent", amount, sender_account["balance"])


def view_transaction_history(account):
    print("\n" + "=" * 50)
    print("              TRANSACTION HISTORY")
    print("=" * 50)

    transactions = account["transactions"]

    if not transactions:
        print("No transactions found.")
        return

    # Show newest transactions first.
    for index, transaction in enumerate(reversed(transactions), start=1):
        display_transaction(index, transaction)


def display_transaction(index, transaction):
    print(f"{index}. {transaction['type']}")
    print(f"   Amount: ${transaction['amount']:.2f}")
    print(f"   Balance After: ${transaction['balance_after']:.2f}")
    print(f"   Note: {transaction['note']}")
    print(f"   Date/Time: {transaction['date_time']}")
    print("-" * 50)


def filter_transactions(account):
    print("\nFilter/Search Transactions")
    print("-" * 50)
    print("1. View All Transactions")
    print("2. Deposits Only")
    print("3. Withdrawals Only")
    print("4. Transfers Only")
    print("5. Search by Keyword")
    print("6. Search by Month")
    print("7. Go Back")

    choice = get_menu_choice(["1", "2", "3", "4", "5", "6", "7"])

    transactions = account["transactions"]

    if choice == "7":
        return

    if not transactions:
        print("No transactions found.")
        return

    if choice == "1":
        filtered = transactions

    elif choice == "2":
        filtered = [
            transaction for transaction in transactions
            if transaction["type"] == "Deposit"
        ]

    elif choice == "3":
        filtered = [
            transaction for transaction in transactions
            if transaction["type"] == "Withdrawal"
        ]

    elif choice == "4":
        filtered = [
            transaction for transaction in transactions
            if "Transfer" in transaction["type"]
        ]

    elif choice == "5":
        keyword = input("Enter keyword to search: ").strip().lower()

        filtered = [
            transaction for transaction in transactions
            if keyword in transaction["type"].lower()
            or keyword in transaction["note"].lower()
            or keyword in transaction["date_time"].lower()
        ]

    elif choice == "6":
        month = input("Enter month in YYYY-MM format, example 2026-05: ").strip()

        filtered = [
            transaction for transaction in transactions
            if transaction["date_time"].startswith(month)
        ]

    if not filtered:
        print("No transactions matched your search/filter.")
        return

    print("\n" + "=" * 50)
    print("              FILTERED TRANSACTIONS")
    print("=" * 50)

    for index, transaction in enumerate(reversed(filtered), start=1):
        display_transaction(index, transaction)


def export_monthly_statement(account):
    print("\nExport Monthly Statement")
    print("-" * 50)

    month = input("Enter month in YYYY-MM format, example 2026-05 (or type 'b' to go back): ").strip()

    if is_back_choice(month):
        print("Statement export cancelled.")
        return

    monthly_transactions = [
        transaction for transaction in account["transactions"]
        if transaction["date_time"].startswith(month)
    ]

    if not monthly_transactions:
        print("No transactions found for that month.")
        return

    safe_name = account["name"].replace(" ", "_")
    file_name = f"{safe_name}_{month}_statement.txt"

    with open(file_name, "w", encoding="utf-8") as file:
        file.write("=" * 50 + "\n")
        file.write("MONTHLY BANK STATEMENT\n")
        file.write("=" * 50 + "\n")
        file.write(f"Account Holder: {account['name']}\n")
        file.write(f"Account Number: {account['account_number']}\n")
        file.write(f"Statement Month: {month}\n")
        file.write(f"Current Balance: ${account['balance']:.2f}\n")
        file.write(f"Generated On: {get_current_time()}\n")
        file.write("=" * 50 + "\n\n")

        for index, transaction in enumerate(monthly_transactions, start=1):
            file.write(f"{index}. {transaction['type']}\n")
            file.write(f"   Amount: ${transaction['amount']:.2f}\n")
            file.write(f"   Balance After: ${transaction['balance_after']:.2f}\n")
            file.write(f"   Note: {transaction['note']}\n")
            file.write(f"   Date/Time: {transaction['date_time']}\n")
            file.write("-" * 50 + "\n")

    print(f"Monthly statement exported successfully: {file_name}")


def change_pin(accounts, account_number):
    account = accounts[account_number]

    print("\nChange PIN")
    print("-" * 50)

    old_pin = get_valid_pin("Enter your current PIN")

    if old_pin is None:
        print("PIN change cancelled.")
        return

    if old_pin != account["pin"]:
        print("Incorrect current PIN.")
        return

    new_pin = get_valid_pin("Create your new 4-digit PIN")

    if new_pin is None:
        print("PIN change cancelled.")
        return

    if new_pin == old_pin:
        print("New PIN cannot be the same as your old PIN.")
        return

    account["pin"] = new_pin

    add_transaction(
        account,
        "PIN Change",
        0,
        account["balance"],
        "Account PIN was changed"
    )

    save_accounts(accounts)

    print("PIN changed successfully.")


def delete_account(accounts, account_number):
    account = accounts[account_number]

    print("\nDelete Account")
    print("-" * 50)
    print("Warning: This action permanently deletes your account.")
    print("This cannot be undone.")

    pin = get_valid_pin("Enter your PIN to confirm deletion")

    if pin is None:
        print("Account deletion cancelled.")
        return False

    if pin != account["pin"]:
        print("Incorrect PIN. Account deletion cancelled.")
        return False

    confirmation = input("Type DELETE to permanently delete this account: ").strip()

    if confirmation != "DELETE":
        print("Account deletion cancelled.")
        return False

    del accounts[account_number]
    save_accounts(accounts)

    print("Account deleted successfully.")
    return True


def banking_session(accounts, account_number):
    # This loop runs after the user logs in.
    # It keeps the user in the banking menu until they log out or delete the account.
    while True:
        account = accounts[account_number]

        display_banking_menu(account)
        choice = get_menu_choice(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])

        if choice == "1":
            show_balance(account)

        elif choice == "2":
            deposit_money(accounts, account_number)

        elif choice == "3":
            withdraw_money(accounts, account_number)

        elif choice == "4":
            transfer_money(accounts, account_number)

        elif choice == "5":
            view_transaction_history(account)

        elif choice == "6":
            filter_transactions(account)

        elif choice == "7":
            export_monthly_statement(account)

        elif choice == "8":
            change_pin(accounts, account_number)

        elif choice == "9":
            deleted = delete_account(accounts, account_number)

            if deleted:
                print("Returning to main menu...")
                break

        elif choice == "10":
            print("Logging out...")
            break


def main():
    # Load saved account data when the program starts.
    accounts = load_accounts()

    while True:
        display_welcome_menu()
        choice = get_menu_choice(["1", "2", "3"])

        if choice == "1":
            create_account(accounts)

        elif choice == "2":
            account_number = login(accounts)

            if account_number:
                banking_session(accounts, account_number)

        elif choice == "3":
            print("\nThank you for using the Python Banking System.")
            print("Have a nice day!")
            break


if __name__ == "__main__":
    main()
