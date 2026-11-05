from employees.models import department, employee
from django.shortcuts import render


def home(request):
    employees = employee.objects.all()
    context = {
        'employees': employees.order_by('-id')[:8],
        'total_employees': employees.count(),
        'active_employees': employees.filter(is_active=True).count(),
        'inactive_employees': employees.filter(is_active=False).count(),
        'total_departments': department.objects.count(),
    }
    return render(request, 'home.html', context)
