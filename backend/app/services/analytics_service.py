from collections import defaultdict
from datetime import date
from math import ceil
from typing import Iterable, Optional

from app.models import Transaction


INCOME_CATEGORIES = {"INCOME", "TRANSFER_IN"}
DEBT_KEYWORDS = ("loan", "student", "credit card", "card payment", "mortgage", "debt")


def total_income(transactions: Iterable[Transaction]) -> float:
    return round(sum(abs(t.amount) for t in transactions if is_income(t)), 2)


def total_expenses(transactions: Iterable[Transaction]) -> float:
    return round(sum(t.amount for t in transactions if is_expense(t)), 2)


def net_cash_flow(transactions: Iterable[Transaction]) -> float:
    txs = list(transactions)
    return round(total_income(txs) - total_expenses(txs), 2)


def savings_rate(transactions: Iterable[Transaction]) -> float:
    txs = list(transactions)
    income = total_income(txs)
    if income <= 0:
        return 0
    return round((net_cash_flow(txs) / income) * 100, 2)


def monthly_income_vs_expenses(transactions: Iterable[Transaction]) -> list[dict]:
    buckets: dict[str, dict[str, float]] = defaultdict(lambda: {"income": 0.0, "expenses": 0.0})
    for tx in transactions:
        month = tx.date.strftime("%Y-%m")
        if is_income(tx):
            buckets[month]["income"] += abs(tx.amount)
        elif is_expense(tx):
            buckets[month]["expenses"] += tx.amount
    return [
        {
            "month": month,
            "income": round(values["income"], 2),
            "expenses": round(values["expenses"], 2),
            "net": round(values["income"] - values["expenses"], 2),
        }
        for month, values in sorted(buckets.items())
    ]


def category_spending(transactions: Iterable[Transaction]) -> list[dict]:
    buckets: dict[str, float] = defaultdict(float)
    for tx in transactions:
        if is_expense(tx):
            buckets[tx.category_primary or "Other"] += tx.amount
    return [{"category": k, "amount": round(v, 2)} for k, v in sorted(buckets.items(), key=lambda item: item[1], reverse=True)]


def top_merchants(transactions: Iterable[Transaction], limit: int = 10) -> list[dict]:
    buckets: dict[str, float] = defaultdict(float)
    for tx in transactions:
        if is_expense(tx):
            buckets[tx.merchant_name or tx.name] += tx.amount
    ranked = sorted(buckets.items(), key=lambda item: item[1], reverse=True)[:limit]
    return [{"merchant": merchant, "amount": round(amount, 2)} for merchant, amount in ranked]


def recurring_transactions(transactions: Iterable[Transaction]) -> list[dict]:
    grouped: dict[tuple[str, int], list[Transaction]] = defaultdict(list)
    for tx in transactions:
        if is_expense(tx):
            grouped[((tx.merchant_name or tx.name).lower(), round(tx.amount))].append(tx)

    recurring = []
    for (merchant, rounded_amount), rows in grouped.items():
        months = {row.date.strftime("%Y-%m") for row in rows}
        if len(months) >= 2 and len(rows) >= 2:
            recurring.append(
                {
                    "merchant": merchant.title(),
                    "amount": round(sum(row.amount for row in rows) / len(rows), 2),
                    "frequency": "monthly",
                    "count": len(rows),
                    "last_seen": max(row.date for row in rows).isoformat(),
                    "category": rows[0].category_primary,
                }
            )
    return sorted(recurring, key=lambda item: item["amount"], reverse=True)


def month_over_month_comparison(transactions: Iterable[Transaction]) -> dict[str, float]:
    monthly = monthly_income_vs_expenses(transactions)
    if len(monthly) < 2:
        return {"income_change": 0, "expense_change": 0, "net_change": 0}
    previous, current = monthly[-2], monthly[-1]
    return {
        "income_change": percent_change(previous["income"], current["income"]),
        "expense_change": percent_change(previous["expenses"], current["expenses"]),
        "net_change": round(current["net"] - previous["net"], 2),
    }


def debt_payment_total(transactions: Iterable[Transaction]) -> float:
    return round(sum(tx.amount for tx in transactions if is_debt_payment(tx)), 2)


def debt_payoff_calculator(balance: float, annual_rate: float, monthly_payment: float) -> dict:
    if monthly_payment <= 0:
        return {"monthly_payment": monthly_payment, "months": None, "total_interest": 0, "payoff_date": None}
    monthly_rate = annual_rate / 100 / 12
    remaining = balance
    total_interest = 0.0
    months = 0
    while remaining > 0 and months < 1200:
        interest = remaining * monthly_rate
        principal = monthly_payment - interest
        if principal <= 0:
            return {"monthly_payment": monthly_payment, "months": None, "total_interest": round(total_interest, 2), "payoff_date": None}
        remaining -= principal
        total_interest += interest
        months += 1
    payoff_year = date.today().year + (date.today().month + months - 1) // 12
    payoff_month = (date.today().month + months - 1) % 12 + 1
    return {
        "monthly_payment": round(monthly_payment, 2),
        "months": months,
        "total_interest": round(total_interest, 2),
        "payoff_date": f"{payoff_year}-{payoff_month:02d}",
    }


def summarize_for_ai(transactions: Iterable[Transaction]) -> dict:
    txs = list(transactions)
    return {
        "summary": {
            "income": total_income(txs),
            "expenses": total_expenses(txs),
            "net_cash_flow": net_cash_flow(txs),
            "savings_rate": savings_rate(txs),
            "debt_payments": debt_payment_total(txs),
            "month_over_month": month_over_month_comparison(txs),
        },
        "monthly_totals": monthly_income_vs_expenses(txs),
        "category_totals": category_spending(txs),
        "merchant_totals": top_merchants(txs, limit=8),
        "recurring_expenses": recurring_transactions(txs),
    }


def is_income(tx: Transaction) -> bool:
    return tx.amount < 0 or (tx.category_primary or "").upper() in INCOME_CATEGORIES


def is_expense(tx: Transaction) -> bool:
    return tx.amount > 0 and not tx.pending


def is_debt_payment(tx: Transaction) -> bool:
    haystack = f"{tx.name} {tx.merchant_name} {tx.category_primary} {tx.category_detailed}".lower()
    return is_expense(tx) and any(keyword in haystack for keyword in DEBT_KEYWORDS)


def percent_change(previous: float, current: float) -> float:
    if previous == 0:
        return 0
    return round(((current - previous) / previous) * 100, 2)
