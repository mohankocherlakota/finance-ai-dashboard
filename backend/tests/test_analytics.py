from datetime import date

from app.models import Transaction
from app.services.analytics_service import (
    category_spending,
    debt_payoff_calculator,
    monthly_income_vs_expenses,
    net_cash_flow,
    recurring_transactions,
    savings_rate,
    total_expenses,
    total_income,
)


def tx(day: str, name: str, amount: float, category: str = "FOOD_AND_DRINK") -> Transaction:
    return Transaction(
        plaid_transaction_id=f"{name}-{day}-{amount}",
        date=date.fromisoformat(day),
        name=name,
        merchant_name=name,
        amount=amount,
        category_primary=category,
        category_detailed=category,
        account_id=1,
        pending=False,
    )


def test_summary_math():
    rows = [
        tx("2026-01-01", "Payroll", -5000, "INCOME"),
        tx("2026-01-02", "Rent", 1800, "RENT_AND_UTILITIES"),
        tx("2026-01-03", "Grocer", 200),
    ]
    assert total_income(rows) == 5000
    assert total_expenses(rows) == 2000
    assert net_cash_flow(rows) == 3000
    assert savings_rate(rows) == 60


def test_monthly_and_category_spending():
    rows = [tx("2026-01-01", "Payroll", -5000, "INCOME"), tx("2026-01-03", "Grocer", 200)]
    assert monthly_income_vs_expenses(rows)[0]["net"] == 4800
    assert category_spending(rows)[0] == {"category": "FOOD_AND_DRINK", "amount": 200}


def test_recurring_detection():
    rows = [tx("2026-01-11", "Netflix", 22.99), tx("2026-02-11", "Netflix", 22.99)]
    assert recurring_transactions(rows)[0]["merchant"] == "Netflix"


def test_debt_payoff_calculator():
    result = debt_payoff_calculator(10000, 6, 500)
    assert result["months"] is not None
    assert result["months"] > 0
