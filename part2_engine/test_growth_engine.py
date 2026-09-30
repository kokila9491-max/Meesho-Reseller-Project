import csv
from pathlib import Path

from part2_engine.growth_engine import is_flagged, mom_growth, validate_feed


FIXTURES_DIR = Path(__file__).parent / "fixtures"


# GIVEN April -> May Ethnic Wear revenue changes from 104520.77 to 185107.61
# WHEN growth and flagging are evaluated
# THEN the growth is 77.1% and the result is flagged.
def test_ethnic_wear_growth_is_flagged():
    growth = mom_growth(104520.77, 185107.61)

    assert growth == 77.1
    assert is_flagged(growth) == "flagged"


# GIVEN May -> June Beauty & Personal Care revenue changes from 35542.11 to 37559.07
# WHEN growth and flagging are evaluated
# THEN the growth is 5.67% and the result is not flagged.
def test_beauty_growth_is_not_flagged():
    growth = mom_growth(35542.11, 37559.07)

    assert growth == 5.67
    assert is_flagged(growth) == "not_flagged"


# GIVEN a pair whose growth is exactly the threshold
# WHEN growth and flagging are evaluated
# THEN the result is held for human review.
def test_exact_threshold_escalates():
    growth = mom_growth(100000, 108000)

    assert growth == 8.0
    assert is_flagged(growth) == "escalate_exact_boundary"
    assert is_flagged(growth) not in {"flagged", "not_flagged"}


# GIVEN the corrupted feed fixture
# WHEN it is validated
# THEN its three errors are returned in file order.
def test_corrupted_feed_returns_expected_errors():
    valid, errors = validate_feed(str(FIXTURES_DIR / "corrupted_feed.csv"))

    assert (valid, errors) == (
        False,
        [
            "line 3: negative revenue (-4200.0) for category=Western Wear",
            "line 4: missing category (month=July)",
            "line 6: missing revenue (category=Home & Kitchen)",
        ],
    )


def test_monthly_category_feed_is_valid():
    valid, errors = validate_feed(str(FIXTURES_DIR / "monthly_category_revenue.csv"))
    with (FIXTURES_DIR / "monthly_category_revenue.csv").open(
        newline="", encoding="utf-8"
    ) as feed:
        row_count = sum(1 for _ in csv.DictReader(feed))

    assert (valid, errors) == (True, [])
    assert row_count == 15


def _monthly_revenue() -> dict[tuple[str, str], float]:
    with (FIXTURES_DIR / "monthly_category_revenue.csv").open(
        newline="", encoding="utf-8"
    ) as feed:
        rows = csv.DictReader(feed)
        return {
            (row["month"], row["category"]): float(row["revenue"])
            for row in rows
        }


def test_may_growth_table():
    revenue = _monthly_revenue()
    expected = {
        "Ethnic Wear": (77.1, "flagged"),
        "Western Wear": (-23.6, "flagged"),
        "Kids Wear": (-23.48, "flagged"),
        "Home & Kitchen": (-9.25, "flagged"),
        "Beauty & Personal Care": (-12.75, "flagged"),
    }
    actual = {
        category: (
            growth := mom_growth(revenue[("April", category)], revenue[("May", category)]),
            is_flagged(growth),
        )
        for category in expected
    }

    assert actual == expected


def test_june_growth_table():
    revenue = _monthly_revenue()
    expected = {
        "Ethnic Wear": (-58.74, "flagged"),
        "Western Wear": (11.97, "flagged"),
        "Kids Wear": (23.9, "flagged"),
        "Home & Kitchen": (42.59, "flagged"),
        "Beauty & Personal Care": (5.67, "not_flagged"),
    }
    actual = {
        category: (
            growth := mom_growth(revenue[("May", category)], revenue[("June", category)]),
            is_flagged(growth),
        )
        for category in expected
    }

    assert actual == expected
