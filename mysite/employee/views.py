from django.shortcuts import render
from employee.models import EmployeeTree
from django.views.generic import ListView


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
    # ordering = context['request']
    # paginate_by = 10
    
   
    def get_ordering(self):
        self.ordering = self.request.GET.get('order_by')
        return self.ordering
