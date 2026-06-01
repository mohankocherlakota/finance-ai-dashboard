from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models import Account, Transaction


MOCK_TRANSACTIONS = [
    ("2026-01-03", "Payroll Deposit", "Acme Corp", -7200, "INCOME", "PAYROLL"),
    ("2026-01-04", "Rent Payment", "North Loop Apartments", 2450, "RENT_AND_UTILITIES", "RENT"),
    ("2026-01-06", "Whole Foods", "Whole Foods", 186.43, "FOOD_AND_DRINK", "GROCERIES"),
    ("2026-01-11", "Netflix", "Netflix", 22.99, "ENTERTAINMENT", "SUBSCRIPTION"),
    ("2026-01-14", "Student Loan Payment", "Federal Loan Servicer", 1700, "LOAN_PAYMENTS", "STUDENT_LOAN"),
    ("2026-01-18", "United Airlines", "United Airlines", 420.1, "TRAVEL", "FLIGHTS"),
    ("2026-02-03", "Payroll Deposit", "Acme Corp", -7200, "INCOME", "PAYROLL"),
    ("2026-02-04", "Rent Payment", "North Loop Apartments", 2450, "RENT_AND_UTILITIES", "RENT"),
    ("2026-02-06", "Whole Foods", "Whole Foods", 211.8, "FOOD_AND_DRINK", "GROCERIES"),
    ("2026-02-09", "Uber", "Uber", 78.4, "TRANSPORTATION", "TAXIS_AND_RIDE_SHARES"),
    ("2026-02-11", "Netflix", "Netflix", 22.99, "ENTERTAINMENT", "SUBSCRIPTION"),
    ("2026-02-14", "Student Loan Payment", "Federal Loan Servicer", 1700, "LOAN_PAYMENTS", "STUDENT_LOAN"),
    ("2026-03-03", "Payroll Deposit", "Acme Corp", -7200, "INCOME", "PAYROLL"),
    ("2026-03-04", "Rent Payment", "North Loop Apartments", 2450, "RENT_AND_UTILITIES", "RENT"),
    ("2026-03-06", "Whole Foods", "Whole Foods", 198.33, "FOOD_AND_DRINK", "GROCERIES"),
    ("2026-03-08", "Blue Bottle", "Blue Bottle", 42.6, "FOOD_AND_DRINK", "COFFEE"),
    ("2026-03-11", "Netflix", "Netflix", 22.99, "ENTERTAINMENT", "SUBSCRIPTION"),
    ("2026-03-14", "Student Loan Payment", "Federal Loan Servicer", 1700, "LOAN_PAYMENTS", "STUDENT_LOAN"),
    ("2026-03-20", "Credit Card Payment", "Chase Card Services", 650, "LOAN_PAYMENTS", "CREDIT_CARD_PAYMENT"),
    ("2026-04-03", "Payroll Deposit", "Acme Corp", -7200, "INCOME", "PAYROLL"),
    ("2026-04-04", "Rent Payment", "North Loop Apartments", 2450, "RENT_AND_UTILITIES", "RENT"),
    ("2026-04-06", "Whole Foods", "Whole Foods", 233.12, "FOOD_AND_DRINK", "GROCERIES"),
    ("2026-04-11", "Netflix", "Netflix", 22.99, "ENTERTAINMENT", "SUBSCRIPTION"),
    ("2026-04-14", "Student Loan Payment", "Federal Loan Servicer", 1700, "LOAN_PAYMENTS", "STUDENT_LOAN"),
    ("2026-04-22", "Apple Store", "Apple", 129.0, "GENERAL_MERCHANDISE", "ELECTRONICS"),
    ("2026-05-03", "Payroll Deposit", "Acme Corp", -7200, "INCOME", "PAYROLL"),
    ("2026-05-04", "Rent Payment", "North Loop Apartments", 2450, "RENT_AND_UTILITIES", "RENT"),
    ("2026-05-06", "Whole Foods", "Whole Foods", 219.44, "FOOD_AND_DRINK", "GROCERIES"),
    ("2026-05-11", "Netflix", "Netflix", 22.99, "ENTERTAINMENT", "SUBSCRIPTION"),
    ("2026-05-14", "Student Loan Payment", "Federal Loan Servicer", 1700, "LOAN_PAYMENTS", "STUDENT_LOAN"),
    ("2026-05-18", "Delta Dental", "Delta Dental", 54.0, "MEDICAL", "INSURANCE"),
    ("2026-05-25", "Brokerage Transfer", "Vanguard", 800, "TRANSFER_OUT", "INVESTMENT"),
]


def list_transactions(db: Session) -> list[Transaction]:
    return db.query(Transaction).order_by(Transaction.date.desc()).all()


def seed_mock_data(db: Session) -> dict:
    account = db.query(Account).filter(Account.plaid_account_id == "mock_checking_001").first()
    if not account:
        account = Account(
            plaid_account_id="mock_checking_001",
            name="Sandbox Checking",
            type="depository",
            subtype="checking",
            mask="0000",
        )
        db.add(account)
        db.flush()

    created = 0
    for idx, row in enumerate(MOCK_TRANSACTIONS, start=1):
        tx_id = f"mock_tx_{idx:04d}"
        exists = db.query(Transaction).filter(Transaction.plaid_transaction_id == tx_id).first()
        if exists:
            continue
        tx_date, name, merchant, amount, category, detail = row
        db.add(
            Transaction(
                plaid_transaction_id=tx_id,
                date=date.fromisoformat(tx_date),
                name=name,
                merchant_name=merchant,
                amount=amount,
                category_primary=category,
                category_detailed=detail,
                account_id=account.id,
                pending=False,
            )
        )
        created += 1
    db.commit()
    return {"accounts": 1, "transactions": created}


def reset_data(db: Session) -> None:
    db.query(Transaction).delete()
    db.query(Account).delete()
    db.commit()
