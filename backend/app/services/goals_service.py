from app.services.analytics_service import debt_payoff_calculator


def calculate_debt_scenarios(balance: float, interest_rate: float, monthly_payment: float, extra_payment: float) -> dict:
    requested_payment = monthly_payment + extra_payment
    return {
        "baseline": debt_payoff_calculator(balance, interest_rate, monthly_payment),
        "requested": debt_payoff_calculator(balance, interest_rate, requested_payment),
        "scenarios": [
            debt_payoff_calculator(balance, interest_rate, 1700),
            debt_payoff_calculator(balance, interest_rate, 3000),
            debt_payoff_calculator(balance, interest_rate, 5000),
        ],
    }
