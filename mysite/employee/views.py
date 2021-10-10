import dateutil.parser
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.generics import ListAPIView

from employee.forms import SignUpForm, LoginForm
from employee.models import EmployeeTree
from django.views.generic import ListView, CreateView, FormView
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.response import Response

from dateutil.parser import parse

from employee.serializers import EmployeeTreeSerializer


def get_all_employees(request):
    object_list = EmployeeTree.objects.all()
    return render(request, 'employee/home.html', {'object_list': object_list})


def get_all_employees_test(request):
    object_list = EmployeeTree.objects.all()
    return render(request, 'employee/test_nest.html', {'object_list': object_list})


class EmployeeTreeApiView(ListAPIView):
    queryset = EmployeeTree.objects.all()

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            serializer = EmployeeTreeSerializer(self.get_queryset(), many=True)
            return Response(serializer.data, content_type='application/json')
        else:
            return super().get(self, request, *args, **kwargs)

    def get_queryset(self):
        if self.request.is_ajax():
            pk = self.request.GET.get('pk')
            children_queryset = EmployeeTree.objects.filter(parent=pk)
            return children_queryset
        else:
            return super().get_queryset()


class EmployeeListApiView(LoginRequiredMixin, ListAPIView):
    queryset = EmployeeTree.objects.all()

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            serializer = EmployeeTreeSerializer(self.get_queryset(), many=True)
            return Response(serializer.data, content_type='application/json')
        else:
            return super().get(self, request, *args, **kwargs)

    def get_queryset(self):
        ordering = self.get_ordering()
        if self.request.GET.get('s'):
            search = self.request.GET.get('s')
            # https://docs.djangoproject.com/en/3.2/topics/db/queries/
            if search.isdigit():
                if ordering:
                    return super().get_queryset().filter(Q(pk=search) | Q(level=search) | Q(salary=search)).order_by(oredering)
                else:
                    return super().get_queryset().filter(Q(pk=search) | Q(level=search) | Q(salary=search))
            elif search.isalpha() or ''.join(search.split()).isalpha():  # Либо введено имя/фамилия, либо и то и то
                if ordering:
                    return super().get_queryset().filter(full_name__icontains=search).order_by(ordering)
                else:
                    return super().get_queryset().filter(full_name__icontains=search)
            else:  # Сюда попадаем если search содержит знаки
                try:
                    date = parse(search).date()
                    if ordering:
                        return super().get_queryset().filter(hired_at=date).order_by(ordering)
                    else:
                        return super().get_queryset().filter(hired_at=date)
                except dateutil.parser.ParserError:
                    return None
        else:
            return super().get_queryset().order_by(ordering)

    def get_ordering(self):
        print(f"I was here {self.request.GET.get('order_by')}")
        self.ordering = self.request.GET.get('order_by')
        return self.ordering

# class EmployeeListApi1View(ListAPIView):
#
#     def get(self, request, *args, **kwargs):
#         if request.is_ajax():
#             serializer = EmployeeTreeSerializer(self.get_queryset(), many=True)
#             return Response(serializer.data, content_type='application/json')
#         else:
#             return super().get(self, request, *args, **kwargs)
class EmployeesListView(LoginRequiredMixin, ListView):
    model = EmployeeTree
    template_name = "employee/employees.html"  # <app>/<model>_<viewtype>.html
    context_object_name = "employees"

    def get_ordering(self):
        self.ordering = self.request.GET.get('order_by')
        return self.ordering


class SignUpView(CreateView):
    model = User
    template_name = 'employee/signup.html'
    form_class = SignUpForm

    def get_success_url(self):
        return reverse('employees-home')


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'employee/login.html'

    def get_success_url(self):
        return reverse('employees-home')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect(self.get_success_url())


def user_logout(request):
    logout(request)
    return redirect('employees-home')
