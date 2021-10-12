import mptt
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from PIL import Image


class EmployeeTree(MPTTModel):
    class Meta:
        db_table = 'employee_tree'
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    full_name = models.CharField(max_length=150)
    level = models.IntegerField()
    hired_at = models.DateField()
    salary = models.IntegerField()
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.PROTECT)
    image = models.ImageField(default ='default.jpg', upload_to = 'employees_foto')


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


    def __str__(self):
        return self.full_name


    class MPTTMeta:
        order_insertion_by = ['full_name']


mptt.register(EmployeeTree, order_insertion_by=['full_name'])



    
