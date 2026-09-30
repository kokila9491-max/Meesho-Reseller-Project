# Flagged Category Narrative Prompt Pack

## Trigger

Start this prompt only when a category's `is_flagged` result is exactly `"flagged"`.

## Input List

- `{category}`: the category with the flagged movement.
- `{previous_revenue}`: revenue for the prior month.
- `{current_revenue}`: revenue for the current month.
- `{mom_pct}`: the calculated month-on-month growth percentage.
- `{prev_month}`: the prior month name.
- `{month}`: the current month name.
- `{reseller_alias}`: an optional coded reseller alias, if a reseller is relevant to the supplied context.

## Prompt

You are writing a concise business narrative about a flagged category movement.

Use the supplied context exactly: `{category}` revenue changed from `{previous_revenue}` in `{prev_month}` to `{current_revenue}` in `{month}`, producing month-on-month growth of `{mom_pct}%`.

Structure the response under exactly these headings:

**Context**
State the supplied category, months, revenue values, and growth percentage as facts.

**Insight**
Explain the business meaning of the movement. Label any interpretation that is not directly supplied as **Hypothesis**. Do not present an unsupported cause as fact.

**Implication**
Give one specific, actionable recommendation tied to the flagged movement. Keep the recommendation operational and concise.

Narrative rules:

- State no number, percentage, date, count, or monetary value that is not supplied through a placeholder.
- Do not calculate, round, infer, or invent additional numeric values.
- Use `{prev_month}` and `{month}` explicitly when naming the comparison.
- If a reseller is referenced, use only `{reseller_alias}` and never a raw reseller name.
- Do not claim that a cause is confirmed unless it is supplied as an input fact.

## Validation Checklist

Before using the draft, confirm all of the following:

- Every number in the draft matches one of the supplied placeholder values exactly.
- Every claim is labeled as a **Fact** or **Hypothesis**, as appropriate.
- The recommendation is specific and actionable rather than vague.
- Any reseller reference uses only the coded `{reseller_alias}` and never a raw reseller name.
- The response contains the required **Context**, **Insight**, and **Implication** headings.
