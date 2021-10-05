from django.urls import path
from .views import EmployeesListView
from employee.views import get_all_employees, get_all_employees_test

urlpatterns = [
    path('', get_all_employees, name="employees-home"),
    path('test/', get_all_employees_test, name="employees-test"),
    path('employees/', EmployeesListView.as_view(), name="employees-detail")
]