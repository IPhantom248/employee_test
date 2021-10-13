import sys

import dateutil.parser
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.functional import cached_property
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.utils.urls import replace_query_param, remove_query_param

from employee.forms import SignUpForm, LoginForm, EmployeesEditForm
from employee.models import EmployeeTree
from django.views.generic import ListView, CreateView, FormView, DeleteView, UpdateView
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


class EmployeesEditView(UpdateView):
    model = EmployeeTree
    template_name = 'employee/edit.html'
    form_class = EmployeesEditForm
    success_url = reverse_lazy('employees-detail')

    # def form_valid(self, form):
    #     obj = form.save(commit=False)
    #     print(obj.parent)
    #     self.object = form.save()
    #     return HttpResponseRedirect(self.get_success_url())


class EmployeesDeleteView(DeleteView):
    model = EmployeeTree
    template_name = 'employee/delete.html'
    success_url = reverse_lazy('employees-detail')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_leaf_node():
            return super().delete(self, request, *args, **kwargs)
        else:
            parent = self.object.parent
            children = self.object.get_children()
            for child in children:
                child.move_to(parent, position='first-child')
            self.object.delete()
            success_url = self.get_success_url()
            return HttpResponseRedirect(success_url)


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



class SmallResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'



    def get_paginated_response(self, data):
        url = self.request.build_absolute_uri()
        last_link = replace_query_param(url, self.page_query_param, 'last')
        first_link = remove_query_param(url, self.page_query_param)
        if first_link == url:
            first_link = None
        if last_link == url:
            last_link = None
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        })


class EmployeeListApiView(LoginRequiredMixin, ListAPIView):
    queryset = EmployeeTree.objects.all()
    pagination_class = SmallResultsSetPagination

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            serializer = EmployeeTreeSerializer(self.get_queryset(), many=True)
            page = self.paginate_queryset(serializer.data)
            # return Response(serializer.data, content_type='application/json')
            return self.get_paginated_response(page)
        else:
            return super().get(self, request, *args, **kwargs)

    def get_queryset(self):
        ordering = self.get_ordering()
        if self.request.GET.get('s'):
            search = self.request.GET.get('s')
            # https://docs.djangoproject.com/en/3.2/topics/db/queries/
            if search.isdigit():
                if ordering:
                    return super().get_queryset().filter(Q(pk=search) | Q(level=search) | Q(salary=search)).order_by(ordering)
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
            return super().get_queryset()

    def get_ordering(self):
        self.ordering = self.request.GET.get('order_by')
        return self.ordering


class EmployeesListView(LoginRequiredMixin, ListView):
    model = EmployeeTree
    login_url = 'login'
    template_name = "employee/employees.html"  # <app>/<model>_<viewtype>.html
    context_object_name = "employees"
    paginate_by = 10

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
