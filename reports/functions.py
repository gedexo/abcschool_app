from datetime import date, datetime, timedelta
from decimal import Decimal

from fees.models import AdditionalFeeStudent
from students.models import StudentFeeStatement


def month_to_number(month_name):
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    return months.index(month_name) + 1


def get_fee(student_fee, fee_type):
    qs = AdditionalFeeStudent.objects.filter(
        academic_year=student_fee.academic_year,
        student=student_fee.student,
        fee=fee_type,
        is_active=True,
    )
    return sum([item.amount for item in qs])


def get_due_fee(academic_year_student_fee, month):
    fee_structure = academic_year_student_fee.generate_fee_structure()
    current_month_number = datetime.now().month
    specified_month_number = month_to_number(month)

    for fee_entry in fee_structure:
        fee_month = month_to_number(fee_entry["month"])

        if current_month_number == 1 and specified_month_number in (
            7,
            8,
            9,
            10,
            11,
            12,
        ):
            return fee_entry["fee"]
        elif current_month_number == 2 and specified_month_number == 1:
            return fee_entry["fee"]
        elif current_month_number == 2 and specified_month_number in (
            1,
            7,
            8,
            9,
            10,
            11,
            12,
        ):
            return fee_entry["fee"]
        elif current_month_number in (3, 4, 5, 6):
            return fee_entry["fee"]
        elif specified_month_number == 1 and current_month_number == 1:
            if fee_month >= 7:
                return fee_entry["fee"]
        elif specified_month_number == 2 and current_month_number == 2:
            if fee_month >= 7:
                return fee_entry["fee"]
        elif 1 <= specified_month_number <= 2 and 7 <= fee_month <= 12:
            return Decimal("0.00")
        else:
            if fee_month <= current_month_number and fee_entry["month"] == month:
                return fee_entry["fee"]

    # If no matching condition is found, return 0.00
    return Decimal("0.00")


def monthly_student_fee_receipt(academic_year_student, month):
    qs = StudentFeeStatement.objects.filter(
        academic_year=academic_year_student.academic_year,
        student=academic_year_student.student,
        date__month=month,
        is_active=True,
    )
    return sum([item.amount for item in qs])


def get_year_month_set(startdate, enddate):
    current_date = startdate
    unique_months = set()
    while current_date <= enddate:
        unique_months.add((current_date.year, current_date.month))
        current_date = date(current_date.year, current_date.month, 1) + timedelta(days=32)
        unique_months_list = list(unique_months)
        return unique_months_list


def get_academic_years(startdate, enddate):
    if startdate.month < 6:
        start_year = startdate.year - 1
    else:
        start_year = startdate.year
    if enddate.month < 6:
        end_year = enddate.year - 1
    else:
        end_year = enddate.year
    academic_years = [f"{year}-{year+1}" for year in range(start_year, end_year + 1)]
    return academic_years
