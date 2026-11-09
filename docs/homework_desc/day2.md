# OOP Basics

## Day 2

### Day 2 — Advanced bank account types

### Goal of the day
Implement several child account classes with extended features.

### Requirements

#### 1. Inheritance
Create classes:
- `SavingsAccount`
- `PremiumAccount`
- `InvestmentAccount`

#### 2. `SavingsAccount` features
- `min_balance` — minimum remaining balance
- monthly interest rate
- method `apply_monthly_interest()`

#### 3. `PremiumAccount` features
- increased limits
- overdraft support
- fixed commission/fee

#### 4. `InvestmentAccount` features
- investment portfolio stores an amount distributed across asset types
- allowed virtual asset types: `stocks`, `bonds`, `etf`
- method `project_yearly_growth(growth_rates)` calculates expected yearly portfolio growth
- `growth_rates` is passed as a dict: asset type → yearly rate
- for the demo, use conditional rates: stocks — 10%, bonds — 4%, etf — 7%
- validate: allowed asset type, positive amount, and sufficient funds

Important:
- This is a simplified educational model for OOP practice.
- Do not pick real securities, look up investment rules, or fetch quotes.
- No external APIs or database are required; keep data in memory.

#### 5. Polymorphism
Each account type must override:
- `withdraw()`
- `get_account_info()`
- `__str__()`

#### 6. Testing
Create several accounts of each type and run different operations.
