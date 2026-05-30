# Python Banking System
This is a terminal-based Python banking system.
The program allows users to create bank accounts, log in using an account number and PIN, deposit money, withdraw money, transfer funds, view transaction history, filter transactions, export monthly statements, update their PIN, and delete their account.
This project demonstrates core Python programming skills such as functions, dictionaries, JSON file handling, input validation, authentication logic, transaction management, file writing, error handling, and modular program organization.
---

## Features

* Account creation system
* Unique account number generation
* PIN-based login system
* Login attempt limit
* Better account data structure using account numbers as unique IDs
* Show account balance
* Deposit money
* Withdraw money
* Transfer money between accounts
* Transaction history
* Transaction filtering and searching
* Monthly bank statement export
* Change PIN option
* Delete account option
* Back/return option during user actions
* JSON-based account saving
* Date and time tracking for transactions
* Input validation for menus, PINs, and money amounts
* Human-readable comments throughout the code

---

## Project Structure

```text
Python-Banking-System/
│
├── banking_system.py
├── bank_accounts.json
└── README.md
```

### `banking_system.py`

The main Python file that contains the banking system logic, including account creation, login, deposits, withdrawals, transfers, transaction history, filtering, statement export, PIN updates, and account deletion.

### `bank_accounts.json`

Stores saved account data. This file is created automatically when the program runs and an account is created.

### `README.md`

Explains the project, features, structure, and Python concepts demonstrated.

---

## How to Run

Make sure `banking_system.py` is in your project folder.

Run the program with:

```bash
python banking_system.py
```

or:

```bash
python3 banking_system.py
```

---

## How the Program Works

1. The user starts at the main menu.
2. The user can create an account, log in, or exit.
3. When creating an account, the program asks for the account holder's name and a 4-digit PIN.
4. The program generates a unique account number.
5. The user logs in using their account number and PIN.
6. After logging in, the user can deposit, withdraw, transfer money, view history, filter transactions, export statements, change PIN, or delete the account.
7. Account data and transaction history are saved in `bank_accounts.json`.
8. The user can return to previous menus by typing `b`, `back`, or `return` during supported actions.

---

## Technical Concepts Demonstrated

### Functions and Modular Code Organization

The program is divided into focused functions such as `create_account()`, `login()`, `deposit_money()`, `withdraw_money()`, `transfer_money()`, `filter_transactions()`, and `export_monthly_statement()`.

This keeps the code organized, easier to read, and easier to update.

---

### Better Account Data Structure

The program uses account numbers as unique IDs instead of using names as account identifiers.

Example structure:

```json
{
    "123456": {
        "account_number": "123456",
        "name": "Aybars",
        "pin": "1234",
        "balance": 250.0,
        "status": "active",
        "transactions": []
    }
}
```

This is more realistic because multiple people can have the same name, but account numbers should be unique.

---

### Account Number Generation

The program generates a random 6-digit account number when a new account is created.

```python
account_number = str(random.randint(100000, 999999))
```

The program checks that the generated number is not already used before assigning it to a new account.

This demonstrates random number generation, loops, and uniqueness checking.

---

### PIN Login System

Each account has a 4-digit PIN.

The user must enter the correct PIN to log in.

```python
if pin == account["pin"]:
    return account_number
```

This demonstrates simple authentication logic and user input validation.

---

### Login Attempt Limit

The program limits incorrect PIN attempts.

If the user enters the wrong PIN too many times, the program returns to the main menu.

```python
while attempts < MAX_LOGIN_ATTEMPTS:
```

This demonstrates counters, loops, conditionals, and basic security logic.

---

### Deposits and Withdrawals

The user can deposit and withdraw money from their account.

The program checks that the entered amount is valid and that withdrawals do not exceed the account balance.

```python
if amount > account["balance"]:
    print("Insufficient funds.")
```

This demonstrates arithmetic operations, input validation, and business-rule checking.

---

### Money Transfers

The user can transfer money to another account by entering the receiver's account number.

The program checks that:

* The receiver account exists
* The user is not transferring to their own account
* The sender has enough funds

This demonstrates dictionary lookups, conditionals, and updating multiple records in one transaction.

---

### Transaction History

Every deposit, withdrawal, transfer, and PIN change is saved as a transaction.

Example transaction:

```json
{
    "type": "Deposit",
    "amount": 100.0,
    "balance_after": 150.0,
    "note": "Money deposited into account",
    "date_time": "2026-05-30 14:22:10"
}
```

This demonstrates lists of dictionaries and structured data storage.

---

### Transaction Filtering and Searching

The program allows the user to filter transactions by type, keyword, or month.

Examples:

* View deposits only
* View withdrawals only
* View transfers only
* Search by keyword
* Search by month

This demonstrates list comprehensions, string searching, and working with saved data.

Example:

```python
filtered = [
    transaction for transaction in transactions
    if transaction["type"] == "Deposit"
]
```

---

### Monthly Bank Statement Export

The program can export a monthly bank statement as a `.txt` file.

The statement includes account information, current balance, transaction details, and the date the statement was generated.

This demonstrates writing formatted text files using Python.

```python
with open(file_name, "w", encoding="utf-8") as file:
    file.write("MONTHLY BANK STATEMENT\n")
```

---

### JSON File Handling

The program saves all account data to `bank_accounts.json`.

```python
json.dump(accounts, file, indent=4)
```

It also loads saved account data when the program starts.

```python
accounts = load_accounts()
```

This demonstrates persistent data storage, meaning account information is not lost when the program closes.

---

### Error Handling

The program uses `try` and `except` blocks when loading JSON data.

```python
try:
    with open(ACCOUNT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
except json.JSONDecodeError:
    return {}
```

This prevents the program from crashing if the JSON file is empty or incorrectly formatted.

---

### Input Validation

The program validates user input for:

* Menu choices
* Account names
* PINs
* Money amounts
* Account numbers
* Confirmation prompts

For example, money amounts must be valid positive numbers.

```python
try:
    amount = float(amount_text)
except ValueError:
    print("Invalid amount.")
```

This makes the program more reliable and user-friendly.

---

### Back/Return Option

The user can type `b`, `back`, or `return` during many actions to cancel and go back to the previous menu.

```python
BACK_OPTIONS = ["b", "back", "return"]
```

This improves the user experience and demonstrates reusable helper functions.

---

### Change PIN Option

The user can update their PIN after logging in.

The program checks the old PIN first before allowing the user to create a new PIN.

This demonstrates updating saved account data and requiring authentication before sensitive actions.

---

### Delete Account Option

The user can permanently delete their account.

To prevent accidental deletion, the program requires:

* Correct PIN
* Confirmation by typing `DELETE`

```python
del accounts[account_number]
```

This demonstrates dictionary deletion, confirmation logic, and safe handling of destructive actions.

---

### Date and Time Tracking

Each transaction is saved with a timestamp using Python's `datetime` module.

```python
datetime.now().strftime("%Y-%m-%d %H:%M:%S")
```

This makes transaction history and bank statements more realistic.

---

## Python Concepts Practiced

This project demonstrates the following Python concepts:

* Variables
* Constants
* Functions
* Dictionaries
* Lists
* Nested data structures
* Loops
* Conditional statements
* User input
* Input validation
* Random number generation
* File handling
* JSON reading and writing
* Error handling with `try` and `except`
* List comprehensions
* String methods
* Date and time with the `datetime` module
* Modular program organization
* Basic authentication logic
* Data filtering and searching
* Text file export

---

## Standard Libraries Used

This project only uses Python standard libraries.

```python
import json
import os
import random
from datetime import datetime
```

### `json`

Used to save and load account data.

### `os`

Used to check whether files exist.

### `random`

Used to generate unique account numbers.

### `datetime`

Used to save timestamps for transactions and statements.

---

## What I Learned

While building this project, I practiced creating a more complete terminal-based Python application with persistent data storage and account management features.

I learned how to structure a larger program with functions, store and update account data using dictionaries and JSON, validate user input, create simple authentication logic, manage transactions, filter saved data, and export formatted text files.

This project also helped me understand why separating logic into reusable functions makes the program easier to maintain and expand.
