from django.shortcuts import render

from employee.models import EmployeeTree


def get_all_employees(request):
    object_list = EmployeeTree.objects.all()
    return render(request, 'home.html', {'object_list': object_list})
