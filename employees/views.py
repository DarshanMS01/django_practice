from django.contrib.auth.decorators import login_required,permission_required
from django.shortcuts import render, get_object_or_404
from .models import employee
from .forms import employeeform


def employee_dtail(request, id):
    emp = get_object_or_404(employee, id=id)
    return render(
        request,
        'employee_detail.html',
        {'employee': emp}


    )
@login_required
@permission_required('employees.add_employee',raise_exception=True)
def add_employee(request):
    if request.method == 'POST':
        form = employeeform(request.POST,request.FILES)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    form=employeeform()
    context = {'form': form}
    return render(
        request,
        'add_employee.html',
        context
    )

