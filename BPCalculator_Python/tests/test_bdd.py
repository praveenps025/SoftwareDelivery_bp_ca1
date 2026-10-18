"""BDD step definitions for features/bp_category.feature (pytest-bdd).

Each function below is matched to a Given / When / Then line in the feature file.
"""
import re

from pytest_bdd import given, parsers, scenarios, then, when

# run every scenario in the feature file as a test
scenarios("features/bp_category.feature")


# the category is the only form-group that holds plain text (no HTML tags)
def shown_category(page):
    match = re.search(r'<div class="form-group">\s*([^<]+?)\s*</div>', page)
    return match.group(1) if match else None


# --- Given ---

@given("I open the calculator page", target_fixture="page")
def open_calculator(client):
    response = client.get("/")
    assert response.status_code == 200
    return response.get_data(as_text=True)


# --- When ---

@when(parsers.parse("I enter systolic {systolic} and diastolic {diastolic}"),
      target_fixture="page")
def enter_reading(client, systolic, diastolic):
    data = {"BP.Systolic": systolic, "BP.Diastolic": diastolic}
    response = client.post("/", data=data)
    return response.get_data(as_text=True)


@when(parsers.parse("I enter only diastolic {diastolic}"), target_fixture="page")
def enter_only_diastolic(client, diastolic):
    data = {"BP.Systolic": "", "BP.Diastolic": diastolic}
    response = client.post("/", data=data)
    return response.get_data(as_text=True)


# --- Then ---

@then(parsers.parse('I see "{text}"'))
def page_shows(page, text):
    assert text in page


@then(parsers.parse('the category is "{category}"'))
def category_is(page, category):
    assert shown_category(page) == category


@then("no category is shown")
def no_category_shown(page):
    assert shown_category(page) is None
