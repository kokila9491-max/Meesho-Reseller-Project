# Meesho Reseller-Revenue Analysis-Project Guide

## Project Outcome

This project builds a small, reproducible reseller revenue-analysis pipeline. It generates synthetic order data, answers business questions with SQLite, validates monthly category revenue, calculates month-over-month (MoM) movement, and produces a narrative report plus a guarded monitoring-agent draft.

The generated dataset contains 24 resellers and 900 orders across April, May, and June 2026. It is synthetic test data, not production sales data. The data generator uses a fixed random seed, so rerunning it reproduces the same dataset.

## End-to-End Steps

Run commands from the workspace root in PowerShell. The examples use `python`; substitute the selected Python executable if that command is not on `PATH`.

### 1. Generate the dataset

```powershell
python .\part1_sql\generate_dataset.py
```

This writes `orders.csv`, `resellers.csv`, and `meesho_reseller.db` into `part1_sql`. The SQLite database contains `orders` and `resellers` tables. The generator deletes and recreates those generated data files, so skip this step if you need to preserve local edits to them.

### 2. Run the SQL analysis and export results

```powershell
python .\part2_engine\run_queries.py
```

The exporter runs the seven SELECT queries listed below and writes one CSV per query into [part1_sql/output](part1_sql/output). It uses the database created in Step 1.

### 3. Review category growth and validate feeds

The monthly aggregate CSV at [monthly_category_revenue.csv](part2_engine/fixtures/monthly_category_revenue.csv) is the checked-in feed used by the engine tests and agent scenarios. [growth_engine.py](part2_engine/growth_engine.py) supplies three functions:

- `mom_growth(previous, current)` returns the percentage change rounded to two decimals.
- `is_flagged(mom_pct, threshold=8.0)` flags movements whose absolute value is greater than 8%, leaves movements below 8% unflagged, and escalates exactly 8% for human review.
- `validate_feed(csv_path)` checks that categories exist and revenue is present, numeric, and nonnegative.

The fixture results are:

| Comparison | Category | MoM change | Classification |
| --- | --- | ---: | --- |
| April to May | Ethnic Wear | 77.10% | Flagged |
| April to May | Western Wear | -23.60% | Flagged |
| April to May | Kids Wear | -23.48% | Flagged |
| April to May | Home & Kitchen | -9.25% | Flagged |
| April to May | Beauty & Personal Care | -12.75% | Flagged |
| May to June | Ethnic Wear | -58.74% | Flagged |
| May to June | Home & Kitchen | 42.59% | Flagged |
| May to June | Kids Wear | 23.90% | Flagged |
| May to June | Western Wear | 11.97% | Flagged |
| May to June | Beauty & Personal Care | 5.67% | Not flagged |

### 4. Produce the business narrative

[prompt_pack.md](part3_narrative/prompt_pack.md) defines the Context, Insight, and Implication structure and its numeric and privacy guardrails. [prompt_fill.py](part3_narrative/prompt_fill.py) fills a concise narrative from supplied values. [narrative_report.md](part3_narrative/narrative_report.md) contains the completed April-to-May and May-to-June Ethnic Wear narratives, chart recommendations, and a top-reseller narrative.

Reseller identifiers are converted to aliases by [masking.py](part3_narrative/masking.py). The narrative report uses aliases for its top-reseller discussion; the underlying SQL export intentionally retains raw names for analysis and should be handled accordingly.

### 5. Run the guarded monitoring agent

[agent_spec.md](part4_agent/agent_spec.md) describes the workflow. [mock_agent_runner.py](part4_agent/mock_agent_runner.py) validates both monthly CSVs before calculating growth, drafts messages for at most the three largest flagged movements, lists additional flagged categories as suppressed, and holds drafts for human approval. Invalid feeds result in a hard stop with no drafts. The runner does not send email or call an external service.

The command-line interface accepts one CSV for the previous month and one for the current month; each input must contain rows for only that month:

```powershell
python .\part4_agent\mock_agent_runner.py <run-month> <previous-month.csv> <current-month.csv>
```

It prints one JSON object with validation status, drafted categories, suppressed categories, exact-boundary escalations, and action taken. The all-month fixture is used by the automated tests, which split it into per-month temporary CSV files.

### 6. Run the tests

Install `pytest` if it is not available in the selected Python environment, then run:

```powershell
python -m pip install pytest
python -m pytest -q part2_engine\test_growth_engine.py part3_narrative\test_masking.py part4_agent\test_mock_agent_runner.py
```

The tests cover growth calculations, the exact 8% boundary, corrupted-feed validation, alias masking, the April-to-May and May-to-June agent scenarios, draft limits, and numeric traceability.

## SQL Queries Used

These queries are also stored in [queriws.sql](part1_sql/queriws.sql). The executable export definitions are in [run_queries.py](part2_engine/run_queries.py).

### 1. Monthly revenue and order count by category

```sql
SELECT
	month,
	category,
	ROUND(SUM(quantity * unit_price), 2) AS revenue,
	COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY month, category;
```

### 2. Revenue and order count by region

```sql
SELECT
	r.region,
	ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue,
	COUNT(*) AS n_orders
FROM orders AS o
JOIN resellers AS r ON r.reseller_id = o.reseller_id
GROUP BY r.region
ORDER BY r.region;
```

### 3. Top five resellers over the spend threshold

```sql
SELECT
	o.reseller_id,
	r.reseller_name,
	ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders AS o
JOIN resellers AS r ON r.reseller_id = o.reseller_id
GROUP BY o.reseller_id, r.reseller_name
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;
```

### 4. Resellers with no matching orders

```sql
SELECT
	r.reseller_id,
	r.reseller_name,
	r.city,
	r.region
FROM resellers AS r
LEFT JOIN orders AS o ON o.reseller_id = r.reseller_id
WHERE o.order_id IS NULL
ORDER BY r.reseller_id;
```

### 5. Demonstrate `COUNT(*)` versus `COUNT(order_id)` for an unmatched reseller

```sql
SELECT
	r.reseller_id,
	COUNT(*) AS row_count,
	COUNT(o.order_id) AS order_id_count
FROM resellers AS r
LEFT JOIN orders AS o ON o.reseller_id = r.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY r.reseller_id;
```

The left join retains the reseller row, so `COUNT(*)` is 1 while `COUNT(o.order_id)` is 0.

### 6. June delivered average order value

```sql
SELECT
	ROUND(SUM(quantity * unit_price) / COUNT(*), 2) AS aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';
```

### 7. Grand total revenue

```sql
SELECT
	ROUND(SUM(quantity * unit_price), 2) AS grand_total_revenue
FROM orders;
```

## Recorded Results

The checked-in exports report grand total revenue of INR 1,262,066.92 and June delivered AOV of INR 1,267.69. Monthly total revenue is April INR 419,417.43, May INR 444,594.25, and June INR 398,055.24. North has the highest regional total at INR 337,125.46. The top-reseller export includes five resellers above INR 50,000; the narrative presents them only by alias.

## Program Reference

| File | Purpose |
| --- | --- |
| [generate_dataset.py](part1_sql/generate_dataset.py) | Create reproducible orders and resellers CSVs and the SQLite database. |
| [queriws.sql](part1_sql/queriws.sql) | Human-readable source for the seven analysis queries. |
| [run_queries.py](part2_engine/run_queries.py) | Execute SQL queries and export result CSVs. |
| [growth_engine.py](part2_engine/growth_engine.py) | Feed validation, MoM calculation, and threshold classification. |
| [prompt_pack.md](part3_narrative/prompt_pack.md) | Narrative template and output guardrails. |
| [masking.py](part3_narrative/masking.py) | Map reseller IDs to aliases and detect raw-name leaks. |
| [prompt_fill.py](part3_narrative/prompt_fill.py) | Fill a Context/Insight/Implication narrative from provided values. |
| [mock_agent_runner.py](part4_agent/mock_agent_runner.py) | Validate feeds, rank changes, draft and hold category messages, or hard-stop. |
| [narrative_report.md](part3_narrative/narrative_report.md) | Completed narrative analysis and chart-choice rationale. |
| [agent_spec.md](part4_agent/agent_spec.md) | Agent plan, guardrails, success conditions, and JSON contract. |
