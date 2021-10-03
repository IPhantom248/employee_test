from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from employee.models import EmployeeTree


class EmployeeTreeAdmin(admin.ModelAdmin):
    fields = ['full_name', 'parent', 'level', 'hired_at', 'salary']


admin.site.register(EmployeeTree, EmployeeTreeAdmin)
