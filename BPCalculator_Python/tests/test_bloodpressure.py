import pytest

from bloodpressure import BloodPressure, BPCategory


@pytest.mark.parametrize("systolic, diastolic, expected", [
    (70, 40, BPCategory.LOW),
    (89, 59, BPCategory.LOW),
    (90, 59, BPCategory.IDEAL),
    (89, 60, BPCategory.IDEAL),
    (100, 60, BPCategory.IDEAL),
    (119, 79, BPCategory.IDEAL),
    (120, 70, BPCategory.PRE_HIGH),
    (110, 80, BPCategory.PRE_HIGH),
    (139, 89, BPCategory.PRE_HIGH),
    (140, 70, BPCategory.HIGH),
    (130, 90, BPCategory.HIGH),
    (190, 100, BPCategory.HIGH),
])
def test_category(systolic, diastolic, expected):
    assert BloodPressure(systolic, diastolic).category == expected


def test_category_display_names():
    assert [c.value for c in BPCategory] == [
        "Low Blood Pressure", "Ideal Blood Pressure",
        "Pre-High Blood Pressure", "High Blood Pressure"]
