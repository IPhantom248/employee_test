from django.core.management import BaseCommand
from faker import Faker
import random
from employee.models import Employee


class Command(BaseCommand):

    def handle(self, *args, **options):
        fake = Faker()
        for i in range(0, 1000):
            Employee.objects.create(full_name=fake.name(), level=random.randint(1, 5), hired_at=fake.date_time(),
                                salary=random.randint(1000, 5000))
        print('Employees added!')
