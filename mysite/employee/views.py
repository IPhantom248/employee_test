import json

import dateutil.parser
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core import serializers

from employee.forms import SignUpForm, LoginForm
from employee.models import EmployeeTree
from django.views.generic import ListView, DetailView, CreateView, FormView, RedirectView
from django.contrib.auth.models import User
from django.db.models import Q

from dateutil.parser import parse


def get_all_employees(request):
    object_list = EmployeeTree.objects.all()
    return render(request, 'employee/home.html', {'object_list': object_list})


def get_all_employees_test(request):
    object_list = EmployeeTree.objects.all()
    return render(request, 'employee/test_nest.html', {'object_list': object_list})


class EmployeesListView(LoginRequiredMixin, ListView):
    model = EmployeeTree
    template_name = "employee/employees.html"  # <app>/<model>_<viewtype>.html
    context_object_name = "employees"

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = serializers.serialize('json', self.get_queryset(),
                                         fields=['full_name', 'parent', 'salary', 'hired_at', 'level'])
            print(data)
            return HttpResponse(data, content_type='application/json')
        else:
            return super().get(self, request, *args, **kwargs)

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
                except dateutil.parser.ParserError:
                    return None
        else:
            return super().get_queryset()


# class LoginForm(form)


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
