Feature: Blood pressure category calculator
  As a patient
  I want to enter my blood pressure reading
  So that I know which blood pressure category I am in

  Background:
    Given I open the calculator page

  Scenario: The page opens with an example reading
    Then the category is "Ideal Blood Pressure"

  Scenario Outline: Calculate the category for a reading
    When I enter systolic <systolic> and diastolic <diastolic>
    Then the category is "<category>"

    Examples:
      | systolic | diastolic | category                |
      | 85       | 55        | Low Blood Pressure      |
      | 89       | 59        | Low Blood Pressure      |
      | 90       | 59        | Ideal Blood Pressure    |
      | 110      | 70        | Ideal Blood Pressure    |
      | 120      | 70        | Pre-High Blood Pressure |
      | 125      | 82        | Pre-High Blood Pressure |
      | 140      | 70        | High Blood Pressure     |
      | 145      | 92        | High Blood Pressure     |

  Scenario: The higher of the two readings decides the category
    When I enter systolic 100 and diastolic 95
    Then the category is "High Blood Pressure"

  Scenario: Systolic must be higher than diastolic
    When I enter systolic 80 and diastolic 90
    Then I see "Systolic must be greater than Diastolic"
    And no category is shown

  Scenario Outline: Readings outside the allowed range are rejected
    When I enter systolic <systolic> and diastolic <diastolic>
    Then I see "<message>"
    And no category is shown

    Examples:
      | systolic | diastolic | message                 |
      | 69       | 60        | Invalid Systolic Value  |
      | 191      | 60        | Invalid Systolic Value  |
      | 120      | 39        | Invalid Diastolic Value |
      | 150      | 101       | Invalid Diastolic Value |

  Scenario: A missing value is reported
    When I enter only diastolic 60
    Then I see "The Systolic field is required."
    And no category is shown
