import datetime

from employees.models import Employee
from students.models import Student


def main_context(request):
    # Greeting with respect to time (Good Morning, Good Afternoon, Good Evening)
    now = datetime.datetime.now()
    hour = now.hour
    if hour < 12:
        greeting = "Good Morning"
    elif hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    current_user = None
    name = None

    if request.user.is_authenticated:
        name = request.user.fullname
        if request.user.usertype == "student" and Student.objects.filter(user=request.user).exists():
            current_user = request.user.student
        elif Employee.objects.filter(user=request.user).exists():
            current_user = request.user.employee
        else:
            pass

    return {
        "domain": request.META["HTTP_HOST"],
        "default_user_avatar": f"https://ui-avatars.com/api/?name={name}&background=e8572e&color=fff&size=128",
        "greeting": greeting,
        "name": name,
        "current_user": current_user,
    }
