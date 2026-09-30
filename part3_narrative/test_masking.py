from pathlib import Path

from part3_narrative.masking import alias_for, assert_no_raw_names_leak


REPORT_PATH = Path(__file__).parent / "narrative_report.md"
RAW_TOP_RESELLER_NAMES = [
    "Mumbai Reseller 1",
    "Mumbai Reseller 4",
    "Hyderabad Reseller 6",
    "Lucknow Reseller 6",
    "Jaipur Reseller 5",
]


def test_alias_format():
    assert alias_for("RS019") == "ALIAS-19"
    assert alias_for("RS006") == "ALIAS-06"


def test_final_narrative_has_no_raw_reseller_names():
    narrative = REPORT_PATH.read_text(encoding="utf-8")

    assert assert_no_raw_names_leak(narrative, RAW_TOP_RESELLER_NAMES) is True


def test_raw_name_is_rejected():
    text_with_raw_name = "West region: Mumbai Reseller 1 requires review."

    assert assert_no_raw_names_leak(
        text_with_raw_name,
        RAW_TOP_RESELLER_NAMES,
    ) is False
