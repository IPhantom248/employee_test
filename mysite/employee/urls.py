from django.urls import path
from employee.views import get_all_employees, get_all_employees_test, EmployeesListView, SignUpView, LoginView, \
    user_logout

urlpatterns = [
    path('', get_all_employees, name="employees-home"),
    path('test/', get_all_employees_test, name="employees-test"),
    path('employees/', EmployeesListView.as_view(), name="employees-detail"),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),

]