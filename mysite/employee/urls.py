from django.urls import path

from employee.views import get_all_employees, get_all_employees_test

urlpatterns = [
    path('', get_all_employees),
    path('test/', get_all_employees_test)
]