import dateutil.parser, json
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from employee.forms import SignUpForm, LoginForm, EmployeesEditForm
from employee.models import EmployeeTree
from django.views.generic import ListView, CreateView, FormView, DeleteView, UpdateView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.response import Response

from dateutil.parser import parse

from employee.serializers import EmployeeTreeSerializer


def get_all_employees(request):
    object_list = EmployeeTree.objects.filter(level=0)
    return render(request, 'employee/home.html', {'object_list': object_list})


def get_all_employees_test(request):
    object_list = EmployeeTree.objects.all()
    return render(request, 'employee/test_nest.html', {'object_list': object_list})


class EmployeesCreateView(CreateView):
    model = EmployeeTree
    template_name = 'employee/create.html'
    form_class = EmployeesEditForm
    success_url = reverse_lazy('employees-detail')


class EmployeesDetailView(DetailView):
    model = EmployeeTree
    template_name = 'employee/detail.html'
    context_object_name = 'employee'

    def get_queryset(self):
        return super().get_queryset().select_related('parent')


class EmployeesEditView(UpdateView):
    model = EmployeeTree
    template_name = 'employee/edit.html'
    form_class = EmployeesEditForm
    success_url = reverse_lazy('employees-detail')


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
            children_queryset = EmployeeTree.objects.filter(parent=pk).select_related('parent')
            return children_queryset
        else:
            return super().get_queryset()


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
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
            page = self.paginate_queryset(self.get_queryset().select_related('parent'))
            serializer = EmployeeTreeSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return super().get(self, request, *args, **kwargs)

    def get_queryset(self):
        ordering = self.get_ordering()
        if self.request.GET.get('s'):
            search = self.request.GET.get('s')
            # https://docs.djangoproject.com/en/3.2/topics/db/queries/
            if search.isdigit():
                queryset = super().get_queryset().filter(Q(pk=search) | Q(level=search) | Q(salary=search))
            elif search.isalpha() or ''.join(search.split()).isalpha():  # ???????? ?????????????? ??????/??????????????, ???????? ?? ???? ?? ????
                queryset = super().get_queryset().filter(full_name__icontains=search)
            else:  # ???????? ???????????????? ???????? search ???????????????? ??????????
                try:
                    date = parse(search).date()
                    queryset = super().get_queryset().filter(hired_at=date)
                except dateutil.parser.ParserError:
                    return None
        else:
            queryset = super().get_queryset()
        if ordering:
            queryset = queryset.order_by(ordering)
        return queryset

    def get_ordering(self):
        self.ordering = self.request.GET.get('order_by')
        return self.ordering


class EmployeesListView(LoginRequiredMixin, ListView):
    model = EmployeeTree
    login_url = 'login'
    template_name = "employee/employees.html"  # <app>/<model>_<viewtype>.html
    context_object_name = "employees"
    paginate_by = 10

    def get_queryset(self):
        return super(EmployeesListView, self).get_queryset().select_related('parent')


class SignUpView(CreateView):
    model = User
    template_name = 'employee/signup.html'
    form_class = SignUpForm

    def get_success_url(self):
        return reverse('employees-home')


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'employee/login.html'
    success_url = 'employees-home'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect(self.get_success_url())


def user_logout(request):
    logout(request)
    return redirect('employees-home')


def update_parent(request):
    emp_id = request.GET.get('emp_id')
    parent_id = request.GET.get('parent_id')
    employee = EmployeeTree.objects.get(id=emp_id)
    employee.parent = None
    if parent_id:
        employee.parent = EmployeeTree.objects.get(id=parent_id)
    employee.save()
    response_data = {'success':1}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
