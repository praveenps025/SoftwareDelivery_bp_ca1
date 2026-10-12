"""Domain model - Python port of BPCalculator/BloodPressure.cs."""
from dataclasses import dataclass
from enum import Enum


# BP categories - the enum value is the display name ([Display(Name=...)] in C#)
class BPCategory(Enum):
    LOW = "Low Blood Pressure"
    IDEAL = "Ideal Blood Pressure"
    PRE_HIGH = "Pre-High Blood Pressure"
    HIGH = "High Blood Pressure"


@dataclass
class BloodPressure:
    SYSTOLIC_MIN = 70
    SYSTOLIC_MAX = 190
    DIASTOLIC_MIN = 40
    DIASTOLIC_MAX = 100

    systolic: int                                       # mmHg
    diastolic: int                                      # mmHg

    # calculate BP category
    @property
    def category(self) -> BPCategory:
        if self.systolic >= 140 or self.diastolic >= 90:
            return BPCategory.HIGH
        if self.systolic >= 120 or self.diastolic >= 80:
            return BPCategory.PRE_HIGH
        if self.systolic >= 90 or self.diastolic >= 60:
            return BPCategory.IDEAL
        return BPCategory.LOW
