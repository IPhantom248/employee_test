from django.urls import path

from employee.views import get_all_employees

urlpatterns = [
    path('', get_all_employees)
]