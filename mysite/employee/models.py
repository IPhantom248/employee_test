import mptt
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class EmployeeTree(MPTTModel):
    class Meta():
        db_table = 'employee_tree'
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    full_name = models.CharField(max_length=150)
    level = models.IntegerField()
    hired_at = models.DateField()
    salary = models.IntegerField()
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

    class MPTTMeta:
        order_insertion_by = ['full_name']


mptt.register(EmployeeTree, order_insertion_by=['full_name'])


