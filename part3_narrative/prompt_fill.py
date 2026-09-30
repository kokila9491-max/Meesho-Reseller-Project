def fill_prompt(
    category: str,
    previous_revenue: float,
    current_revenue: float,
    mom_pct: float,
    previous_month: str,
    month: str,
) -> str:
    return (
        f"Context: {category} revenue moved from {previous_revenue} in "
        f"{previous_month} to {current_revenue} in {month}.\n"
        f"Insight: Fact: month-on-month growth was {mom_pct}%.\n"
        "Implication: Hypothesis: review the category's regional order mix, "
        "stock, pricing, and promotion records before taking action."
    )
