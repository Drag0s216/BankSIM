#BankSIM

A command-line bank account simulator built to apply core OOP principles in a practical scenario. Supports account registration, deposits, withdrawals, transfers, and persistent storage via JSON.

##Features

- Account registration with two account types: `Savings` and `Current`
- Deposit, withdraw, and transfer operations
- Overdraft protection
- Persistent storage using JSON files (`Accounts.json`, `TransactionLogs.json`)
- Transaction logging for every operation (deposit, withdraw, transfer)
- Simple CLI menu for account creation and login

##Tech Stack

Python 3 (json, random)

`Accounts.json` and `TransactionLogs.json` are created automatically on the first register and transaction.

##OOP Principles Demonstrated

**Inheritance**
`SavingsAccount` and `CurrentAccount` both inherit from a `BankAccount` class, overriding `interest` and `overdraftLimit` class attributes to reflect their specific rules (Current accounts allow a 500-unit overdraft, Savings accounts allow 0).

**Polymorphism**
On login, the account type is read from stored data, and the subclass (`SavingsAccount` or `CurrentAccount`) is selected automatically. From that point on, the menu calls the same methods (deposit(), withdraw(), transfer()) regardless of account type.


**Encapsulation**
Account data (balance, transaction history) is never modified directly from outside the class. All reads/writes go through class methods (deposit(), withdraw(), accCheck()).

##How It Works

1. **Register** - creates a new account with a randomly generated UID(1000-9999), prompts for name, age, initial deposit, and account type (Savings/Current).
2. **Login** - looks up the account by UID, reads its stored type, and instantiates the matching class if the account exists.
3. **Menu** - a single set of options (Account Info / Deposit / Withdraw / Transfer / Logout).

4. **Persistence** - all account data is stored in `Accounts.json`; every transaction is appended to `TransactionLogs.json` with a unique transaction ID.



##Challenges

The biggest design lesson from this project was the difference between simulating polymorphism and implementing it. The initial version technically used inheritance, but let the user manually select which subclass's method to run in the CLI, defeating the purpose.

The biggest design lesson from this project was the difference between simulating polymorphism and implementing it - the initial version technically used inheritance, but let the user manually select which subclass's method to run in the CLI, defeating the purpose.
