import pytest

from app import create_app
from forms import BloodPressureForm


# fill in the form as if a user had posted it, then run validation
def submit_form(systolic, diastolic):
    app = create_app("Testing")
    data = {"BP.Systolic": systolic, "BP.Diastolic": diastolic}
    with app.test_request_context("/", method="POST", data=data):
        form = BloodPressureForm()
        form.validate()
        return form


# --- valid readings ---

def test_lowest_allowed_values_are_valid():
    form = submit_form(70, 40)
    assert form.errors == {}


def test_highest_allowed_values_are_valid():
    form = submit_form(190, 100)
    assert form.errors == {}


# --- systolic out of range (allowed: 70 to 190) ---

@pytest.mark.parametrize("systolic", [69, 191])
def test_systolic_out_of_range(systolic):
    form = submit_form(systolic, 60)
    assert form.systolic.errors == ["Invalid Systolic Value"]


# --- diastolic out of range (allowed: 40 to 100) ---

@pytest.mark.parametrize("diastolic", [39, 101])
def test_diastolic_out_of_range(diastolic):
    form = submit_form(150, diastolic)
    assert form.diastolic.errors == ["Invalid Diastolic Value"]


# --- missing or non-numeric values ---

def test_missing_systolic():
    form = submit_form("", 60)
    assert form.systolic.errors == ["The Systolic field is required."]


def test_missing_diastolic():
    form = submit_form(120, "")
    assert form.diastolic.errors == ["The Diastolic field is required."]


@pytest.mark.parametrize("text", ["abc", "12.5"])
def test_systolic_must_be_a_whole_number(text):
    form = submit_form(text, 60)
    assert form.systolic.errors != []


# --- systolic must be greater than diastolic ---

def test_equal_values_are_rejected():
    form = submit_form(80, 80)
    assert form.form_errors == ["Systolic must be greater than Diastolic"]


def test_diastolic_higher_than_systolic_is_rejected():
    form = submit_form(80, 90)
    assert form.form_errors == ["Systolic must be greater than Diastolic"]


def test_comparison_is_skipped_when_a_value_is_missing():
    form = submit_form("", 60)
    assert form.form_errors == []


# --- converting the form to a BloodPressure ---

def test_form_values_are_copied_to_the_model():
    bp = submit_form(130, 85).to_model()
    assert bp.systolic == 130
    assert bp.diastolic == 85
