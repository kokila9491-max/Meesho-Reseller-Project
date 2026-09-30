import csv


def mom_growth(previous: float, current: float) -> float:
	return round((current - previous) / previous * 100, 2)


def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
	absolute_growth = abs(mom_pct)
	if absolute_growth > threshold:
		return "flagged"
	if absolute_growth < threshold:
		return "not_flagged"
	return "escalate_exact_boundary"


def validate_feed(csv_path: str) -> tuple[bool, list[str]]:
	errors: list[str] = []

	with open(csv_path, newline="", encoding="utf-8") as feed:
		reader = csv.DictReader(feed)
		for line_number, row in enumerate(reader, start=2):
			month = row.get("month", "")
			category = row.get("category", "")
			revenue = row.get("revenue", "")

			if not category.strip():
				errors.append(
					f"line {line_number}: missing category (month={month})"
				)

			if not revenue.strip():
				errors.append(
					f"line {line_number}: missing revenue (category={category})"
				)
				continue

			try:
				revenue_value = float(revenue)
			except ValueError:
				errors.append(
					f"line {line_number}: revenue not numeric: {revenue!r}"
				)
				continue

			if revenue_value < 0:
				errors.append(
					f"line {line_number}: negative revenue ({revenue_value}) "
					f"for category={category}"
				)

	return (not errors, errors)
