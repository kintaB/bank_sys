# OOP Basics

## Day 4

### Day 4 — Transaction system

### Goal of the day
Create an extended transaction model and a queue-processing module.

### Requirements

#### 1. Class `Transaction`
- ID, type, amount, currency, commission
- sender, receiver
- status, rejection reason
- timestamps

#### 2. Class `TransactionQueue`
- add transactions
- priority
- delayed operations
- cancel

#### 3. Class `TransactionProcessor`
- commissions
- conversion
- retries
- error recording

#### 4. Rules
- no transfers with a negative balance (except Premium)
- no operations on frozen accounts
- commission for external transfers

#### 5. Testing
Create 10 transactions, put them in the queue, process them.
