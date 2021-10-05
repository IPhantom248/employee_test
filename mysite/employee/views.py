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
    # ordering = ["f"]
    # paginate_by = 6

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["title"] = "Sharu X2"
    #     return context



# full_name = models.CharField(max_length=150)
# level = models.IntegerField()
# hired_at = models.DateField()
# salary = models.IntegerField()
# parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delet