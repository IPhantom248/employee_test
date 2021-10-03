from django.db import models


class Employee(models.Model):
    full_name = models.CharField(max_length=150)
    level = models.IntegerField()
    hired_at = models.DateField()
    salary = models.IntegerField()

