from django.core.management import BaseCommand
from faker import Faker
import random
from employee.models import EmployeeTree


class Command(BaseCommand):

    def handle(self, *args, **options):
        fake = Faker()
        for i in range(0, 100):
            rand_level = random.randint(0, 3)  # По заданию необходимо ограничить дерево 5 уровнями
            if rand_level == 0:
                if random.randint(0, 1):
                    random_parent = None  # На 0 уровне нет родителя
                else:
                    random_parent_queryset = EmployeeTree.objects.filter(level=rand_level)
                    random_parent = random_parent_queryset[random.randint(0, random_parent_queryset.count()-1)]
            else:
                random_parent_queryset = EmployeeTree.objects.filter(level=rand_level)
                random_parent = random_parent_queryset[random.randint(0, random_parent_queryset.count()-1)]
            EmployeeTree.objects.create(full_name=fake.name(), hired_at=fake.date_time(),
                                        salary=random.randint(1000, 5000), parent=random_parent)
            if not i % 10:
                print(i)
        print("Done!")

        # print(random_parent.parent)
        # EmployeeTree.objects.create(full_name=fake.name(), level=random.randint(1, 5), hired_at=fake.date_time(),
        #                             salary=random.randint(1000, 5000), parent=random_parent)
        # print('Employees added!')
