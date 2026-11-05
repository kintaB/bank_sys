# OOP Basics

## Day 1

### Day 1 — Basic bank account model (advanced version)

### Goal of the day
Create an extended abstract bank account model that can serve as a base for more complex account types.

### Requirements

#### 1. Abstract class `AbstractAccount`
Create an abstract class that contains:
- unique account identifier
- owner data
- protected balance
- account status: active, frozen, closed
- abstract methods:
  - `deposit(amount)`
  - `withdraw(amount)`
  - `get_account_info()`

#### 2. Class `BankAccount`
Implement a concrete account type with extended features:
- input data validation
- logical statuses and blocked operations for invalid statuses
- automatic short UUID generation when the account number is missing
- `currency` attribute: `RUB`, `USD`, `EUR`, `KZT`, `CNY`

#### 3. Exceptions
Create custom error classes:
- `AccountFrozenError`
- `AccountClosedError`
- `InvalidOperationError`
- `InsufficientFundsError`

#### 4. Basic operations
Add checks for:
- amount correctness
- account status
- protection against negative values

#### 5. String representation
The `__str__` method must show:
- account type
- client
- last 4 digits of the account number
- status
- balance and currency

#### 6. Testing
Create a demonstration of:
- creating an active and a frozen account
- attempting operations on a frozen account
- valid deposit and withdrawal
