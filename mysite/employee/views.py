import parser

from django.shortcuts import render
from employee.models import EmployeeTree
from django.views.generic import ListView
from django.db.models import Q

from dateutil.parser import parse


def get_all_employees(request):
    object_list = EmployeeTree.objects.all()
    return render(request, 'employee/home.html', {'object_list': object_list})

def get_all_employees_test(request):
    object_list = EmployeeTree.objects.all()
    return render(request, 'employee/test_nest.html', {'object_list': object_list})


class EmployeesListView(ListView):
    model = EmployeeTree
    template_name = "employee/employees.html"  # <app>/<model>_<viewtype>.html
    context_object_name = "employees"

    def get_ordering(self):
        self.ordering = self.request.GET.get('order_by')
        return self.ordering

    def get_queryset(self):
        if self.request.GET.get('s'):
            search = self.request.GET.get('s')
            # https://docs.djangoproject.com/en/3.2/topics/db/queries/
            if search.isdigit():
                return super().get_queryset().filter(Q(pk=search) | Q(level=search) | Q(salary=search))
            elif search.isalpha() or ''.join(search.split()).isalpha():  # Либо введено имя/фамилия, либо и то и то
                return super().get_queryset().filter(full_name__icontains=search)
            else:  # Сюда попадаем если search содержит знаки
                try:
                    date = parse(search).date()
                    return super().get_queryset().filter(hired_at=date)
                except parser.ParserError:
                    pass
        else:
            return super().get_queryset()

