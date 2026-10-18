import pytest

from app import create_app
from forms import BloodPressureForm


@pytest.fixture
def app():
    return create_app("Testing")


def make_form(app, systolic, diastolic):
    data = {"BP.Systolic": systolic, "BP.Diastolic": diastolic}
    with app.test_request_context("/", method="POST", data=data):
        form = BloodPressureForm()
        form.validate()
        return form


@pytest.mark.parametrize("systolic, diastolic", [
    (70, 40),       # both minimums
    (190, 100),     # both maximums
    (71, 40),
    (189, 99),
])
def test_values_inside_range_are_valid(app, systolic, diastolic):
    form = make_form(app, systolic, diastolic)
    assert not form.errors and not form.form_errors


@pytest.mark.parametrize("systolic, message", [
    (69, "Invalid Systolic Value"),
    (191, "Invalid Systolic Value"),
])
def test_systolic_out_of_range(app, systolic, message):
    assert make_form(app, systolic, 60).systolic.errors == [message]


@pytest.mark.parametrize("diastolic, message", [
    (39, "Invalid Diastolic Value"),
    (101, "Invalid Diastolic Value"),
])
def test_diastolic_out_of_range(app, diastolic, message):
    assert make_form(app, 150, diastolic).diastolic.errors == [message]


@pytest.mark.parametrize("value", ["", "abc", "12.5"])
def test_non_integer_systolic_rejected(app, value):
    form = make_form(app, value, 60)
    assert form.systolic.errors
    assert form.to_model().systolic is None


def test_missing_diastolic_message(app):
    form = make_form(app, 120, "")
    assert form.diastolic.errors == ["The Diastolic field is required."]


@pytest.mark.parametrize("systolic, diastolic", [(80, 80), (80, 90)])
def test_systolic_must_be_greater_than_diastolic(app, systolic, diastolic):
    form = make_form(app, systolic, diastolic)
    assert form.form_errors == ["Systolic must be greater than Diastolic"]
    assert not form.errors.get("systolic") and not form.errors.get("diastolic")


def test_cross_field_rule_skipped_when_a_value_is_missing(app):
    assert make_form(app, "", 60).form_errors == []


def test_to_model_returns_posted_values(app):
    bp = make_form(app, 130, 85).to_model()
    assert (bp.systolic, bp.diastolic) == (130, 85)
