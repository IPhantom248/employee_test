from django.urls import path
from employee.views import get_all_employees, get_all_employees_test, EmployeesListView, SignUpView, LoginView, \
    user_logout, EmployeeListApiView, EmployeeTreeApiView, EmployeesDeleteView, EmployeesEditView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', get_all_employees, name="employees-home"),
    path('test/', get_all_employees_test, name="employees-test"),
    path('employees/', EmployeesListView.as_view(), name="employees-detail"),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('employees/api/search/', EmployeeListApiView.as_view(), name="employees-api"),
    path('api/tree/', EmployeeTreeApiView.as_view(), name='employees-api-tree'),
    path('employees/<int:pk>/delete', EmployeesDeleteView.as_view(), name='employees-delete'),
    path('employees/<int:pk>/edit', EmployeesEditView.as_view(), name='employees-edit')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)