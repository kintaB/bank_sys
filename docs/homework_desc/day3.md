# OOP Basics

## Day 3

### Day 3 — Bank system

### Goal of the day
Implement a managing bank class with client support and security features.

### Requirements

#### 1. Class `Client`
- full name, ID, status
- list of account numbers
- contacts
- age check: age >= 18

#### 2. Class `Bank`
Methods:
- `add_client()`
- `open_account()`
- `close_account()`
- `freeze_account()`
- `unfreeze_account()`
- `authenticate_client()`
- `search_accounts()`

#### 3. Protection
- 3 failed login attempts = lockout
- mark suspicious actions
- ban operations from 00:00 to 05:00

#### 4. Extra
- `get_total_balance()`
- `get_clients_ranking()`

#### 5. Testing
Create several clients, open accounts, try logins, freeze accounts.
