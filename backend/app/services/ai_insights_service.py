import json
from typing import Any

from openai import OpenAI

from app.config import get_settings
from app.schemas import InsightResponse


FALLBACK_INSIGHTS = InsightResponse(
    observations=[
        "Income is consistent across the recent months, which makes planning easier.",
        "Housing and debt payments are the largest recurring outflows.",
        "Savings rate is positive but sensitive to travel and discretionary purchases.",
    ],
    risks=[
        "A high fixed-expense base may reduce flexibility during income disruption.",
        "Recurring subscriptions can quietly expand if they are not reviewed monthly.",
        "Debt payoff can slow if extra payments are redirected to discretionary spending.",
    ],
    recommended_actions=[
        "Set a monthly fixed-expense ceiling and review it before each pay cycle.",
        "Move savings or extra debt payments automatically after payroll clears.",
        "Review top merchants and pause any low-value recurring charges.",
    ],
    budget_adjustment="Reduce discretionary food, travel, and entertainment by 8-10% and redirect the difference to savings or debt.",
    debt_payoff_suggestion="Keep the baseline loan payment automatic, then add a fixed extra payment when monthly cash flow is positive.",
    motivational_summary="Small repeatable improvements in recurring costs and debt payments can materially improve your cash flow over time.",
)


def generate_insights(summary: dict) -> InsightResponse:
    settings = get_settings()
    if not settings.openai_api_key:
        return FALLBACK_INSIGHTS

    client = OpenAI(api_key=settings.openai_api_key)
    prompt = (
        "You are a personal finance assistant. Use only the summarized data below, never assume raw transaction details. "
        "Return strict JSON with keys observations, risks, recommended_actions, budget_adjustment, debt_payoff_suggestion, "
        "motivational_summary, disclaimer. Each list must contain exactly three strings. "
        'The disclaimer must be "This is not financial advice."\n\n'
        f"Summarized financial data:\n{json.dumps(summary, indent=2)}"
    )
    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": "You provide practical, conservative financial planning observations from aggregates only."},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content or "{}"
    return InsightResponse.model_validate(normalize_insight_payload(json.loads(content)))


def normalize_insight_payload(payload: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(payload)
    for key in ("observations", "risks", "recommended_actions"):
        value = normalized.get(key, [])
        if isinstance(value, str):
            normalized[key] = [value]
        elif not isinstance(value, list):
            normalized[key] = []
        normalized[key] = [str(item) for item in normalized[key]][:3]

    for key in ("budget_adjustment", "debt_payoff_suggestion", "motivational_summary"):
        value = normalized.get(key, "")
        if isinstance(value, list):
            normalized[key] = " ".join(str(item) for item in value)
        else:
            normalized[key] = str(value)

    normalized["disclaimer"] = "This is not financial advice."
    return normalized
