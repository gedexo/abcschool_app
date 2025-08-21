from datetime import date

GENDER_CHOICES = [
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other"),
]

MARITAL_CHOICES = [
    ("married", "Married"),
    ("single", "Single"),
    ("in_a_relationship", "In a Relationship"),
    ("divorced", "Divorced"),
    ("widowed", "Widowed"),
]
NOTICE_PERIOD_CHOICES = [
    ("0", "0"),
    ("1-15", "15 days or less"),
    ("15-30", "15-30 days"),
    ("31-45", "31-45 days"),
    ("46-60", "46-60 days"),
    ("61-90", "61-90 days"),
    ("90+", "More than 90 days"),
]

EMPLOYMENT_TYPE_CHOICES = (
    ("PERMANENT", "Permanent"),
    ("PROBATION", "Probation"),
    ("CONTRACT", "Contract"),
    ("TEMPORARY", "Temporary"),
)
BLOOD_CHOICES = (
    ("a-positive", "A +Ve"),
    ("b-positive", "B +Ve"),
    ("ab-positive", "AB +Ve"),
    ("o-positive", "O +Ve"),
    ("a-negative", "A -Ve"),
    ("b-negative", "B -Ve"),
    ("ab-negative", "AB -Ve"),
    ("o-negative", "O -Ve"),
)
RESIDENCE_CHOICES = (
    ("SELF_OWNED", "Self Owned"),
    ("FAMILY_OWNED", "Family Owned"),
    ("SELF_RENTED", "Self Rented"),
    ("FAMILY_RENTED", "Family Rented"),
    ("COMPANY_RENTED", "Company Rented"),
    ("COMPANY_OWNED", "Company Owned"),
    ("SHARED", "Shared"),
    ("OTHER", "Other"),
)
BRANCH_CHOICES = (
    ("own_branch", "Own Branch"),
    ("franchise", "Franchise"),
)
ATTENDANCE_STATUS_CHOICES = (
    ("present", "Present"),
    ("absent", "Absent"),
)
LEAVE_STATUS = (
    ("pending", "Pending"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
)

EXPENSE_TYPE_CHOICE = (("own", "Own"), ("receivable", "Receivable"))

MONTH_CHOICES = (
    (1, "January"),
    (2, "February"),
    (3, "March"),
    (4, "April"),
    (5, "May"),
    (6, "June"),
    (7, "July"),
    (8, "August"),
    (9, "September"),
    (10, "October"),
    (11, "November"),
    (12, "December"),
)
YEAR_CHOICES = [(i, i) for i in range(2023, date.today().year + 2)]
INCOME_ACCOUNT_CHOICE = (
    ("monthly_charges", "Monthly Charges"),
    ("others", "Others"),
)


FEE_CHOICES = (
    ("uniform_fee", "Uniform Fee"),
    ("book_fee", "Book Fee"),
    ("worksheet_fee", "Worksheet Fee"),
    ("pta_fee", "Pta Fee"),
    ("other", "Other Fee"),
)

TASK_STATUS_CHOICE = [
    ("assigned", "Assigned"),
    ("in_review", "In Review"),
    ("completed", "Completed"),
    ("rework", "Rework"),
]
LEAVE_STATUS_CHOICE = (
    ("pending", "Pending"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
)

LEAVE_TYPE_CHOICES = (
    ("sick", "Sick Leave"),
    ("personal", "Personal Leave"),
    ("vacation", "Vacation Leave"),
    ("others", "Other"),
)
ACADEMIC_YEAR_CHOICES = [(f"{i}-{i+1}", f"{i}-{i+1}") for i in range(2023, date.today().year + 2)]
