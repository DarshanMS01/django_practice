from django.http import HttpResponse
from employees.models import employee
from django.shortcuts import render

def home(request):
    employees = employee.objects.all()
    context = {'employees': employees}
    return render(request, 'home.html', context)   
