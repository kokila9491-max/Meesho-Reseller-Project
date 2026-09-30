import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from part2_engine.growth_engine import is_flagged, mom_growth, validate_feed
from part3_narrative.prompt_fill import fill_prompt


def _read_revenue_feed(csv_path: str) -> dict[str, float]:
    with open(csv_path, newline="", encoding="utf-8") as feed:
        return {
            row["category"]: float(row["revenue"])
            for row in csv.DictReader(feed)
        }


def _result(
    run_month: str,
    validation_status: str,
    validation_errors: list[str],
    flagged_categories: list[dict],
    suppressed_categories: list[str],
    escalated_categories: list[str],
    action_taken: str,
) -> dict:
    return {
        "run_month": run_month,
        "validation_status": validation_status,
        "validation_errors": validation_errors,
        "flagged_categories": flagged_categories,
        "suppressed_categories": suppressed_categories,
        "escalated_categories": escalated_categories,
        "action_taken": action_taken,
    }


def run(month: str, previous_month_csv: str, current_month_csv: str) -> dict:
    current_valid, current_errors = validate_feed(current_month_csv)
    if not current_valid:
        return _result(
            month,
            "invalid",
            current_errors,
            [],
            [],
            [],
            "hard_stop",
        )

    previous_valid, previous_errors = validate_feed(previous_month_csv)
    if not previous_valid:
        return _result(
            month,
            "invalid",
            previous_errors,
            [],
            [],
            [],
            "hard_stop",
        )

    previous_revenue = _read_revenue_feed(previous_month_csv)
    current_revenue = _read_revenue_feed(current_month_csv)
    previous_month = _read_month(previous_month_csv)
    categories = sorted(current_revenue)
    flagged = []
    suppressed = []
    escalated = []

    for category in categories:
        mom_pct = mom_growth(previous_revenue[category], current_revenue[category])
        status = is_flagged(mom_pct)
        item = {
            "category": category,
            "mom_pct": mom_pct,
            "previous_revenue": previous_revenue[category],
            "current_revenue": current_revenue[category],
        }
        if status == "flagged":
            flagged.append(item)
        elif status == "escalate_exact_boundary":
            escalated.append(category)

    flagged.sort(key=lambda item: abs(item["mom_pct"]), reverse=True)
    drafted = []
    for item in flagged[:3]:
        item["drafted"] = True
        item["message"] = fill_prompt(
            item["category"],
            item["previous_revenue"],
            item["current_revenue"],
            item["mom_pct"],
            previous_month,
            month,
        )
        drafted.append(item)

    for item in flagged[3:]:
        suppressed.append(item["category"])

    return _result(
        month,
        "valid",
        [],
        drafted,
        suppressed,
        escalated,
        "drafted_and_held_for_approval",
    )


def _read_month(csv_path: str) -> str:
    with open(csv_path, newline="", encoding="utf-8") as feed:
        first_row = next(csv.DictReader(feed))
    return first_row["month"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the guarded monitoring agent.")
    parser.add_argument("month")
    parser.add_argument("previous_month_csv")
    parser.add_argument("current_month_csv")
    arguments = parser.parse_args()
    output = run(
        arguments.month,
        arguments.previous_month_csv,
        arguments.current_month_csv,
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
