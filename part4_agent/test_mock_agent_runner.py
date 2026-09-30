import csv
import re
import tempfile
from pathlib import Path

from part4_agent.mock_agent_runner import run


FIXTURES_DIR = Path(__file__).parents[1] / "part2_engine" / "fixtures"
FIXTURE = FIXTURES_DIR / "monthly_category_revenue.csv"
CORRUPTED = FIXTURES_DIR / "corrupted_feed.csv"
TOP_LEVEL_KEYS = {
    "run_month",
    "validation_status",
    "validation_errors",
    "flagged_categories",
    "suppressed_categories",
    "escalated_categories",
    "action_taken",
}


def _month_fixture(month: str) -> str:
    with FIXTURE.open(newline="", encoding="utf-8") as source:
        rows = [row for row in csv.DictReader(source) if row["month"] == month]

    temporary = tempfile.NamedTemporaryFile(
        mode="w",
        newline="",
        suffix=".csv",
        delete=False,
    )
    writer = csv.DictWriter(
        temporary,
        fieldnames=["month", "category", "revenue", "n_orders"],
    )
    writer.writeheader()
    writer.writerows(rows)
    temporary.close()
    return temporary.name


def test_may_scenario():
    result = run("May", _month_fixture("April"), _month_fixture("May"))

    assert result.keys() == TOP_LEVEL_KEYS
    assert result["validation_status"] == "valid"
    assert [item["category"] for item in result["flagged_categories"]] == [
        "Ethnic Wear",
        "Western Wear",
        "Kids Wear",
    ]
    assert [item["mom_pct"] for item in result["flagged_categories"]] == [
        77.1,
        -23.6,
        -23.48,
    ]
    assert result["suppressed_categories"] == [
        "Beauty & Personal Care",
        "Home & Kitchen",
    ]
    assert result["escalated_categories"] == []


def test_june_scenario():
    result = run("June", _month_fixture("May"), _month_fixture("June"))

    assert [item["category"] for item in result["flagged_categories"]] == [
        "Ethnic Wear",
        "Home & Kitchen",
        "Kids Wear",
    ]
    assert [item["mom_pct"] for item in result["flagged_categories"]] == [
        -58.74,
        42.59,
        23.9,
    ]
    assert result["suppressed_categories"] == ["Western Wear"]
    assert result["escalated_categories"] == []
    assert "Beauty & Personal Care" not in result["suppressed_categories"]


def test_corrupted_feed_is_a_hard_stop():
    result = run("May", _month_fixture("April"), str(CORRUPTED))

    assert result["validation_status"] == "invalid"
    assert result["action_taken"] == "hard_stop"
    assert result["validation_errors"] == [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)",
    ]
    assert result["flagged_categories"] == []
    assert result["suppressed_categories"] == []


def test_drafted_messages_use_only_supplied_numbers():
    result = run("May", _month_fixture("April"), _month_fixture("May"))

    for item in result["flagged_categories"]:
        assert item["drafted"] is True
        assert item["category"] in item["message"]
        assert str(item["mom_pct"]) + "%" in item["message"]
        numbers = set(re.findall(r"-?\d+(?:\.\d+)?", item["message"]))
        allowed = {
            str(item["mom_pct"]),
            str(item["previous_revenue"]),
            str(item["current_revenue"]),
        }
        assert numbers <= allowed
