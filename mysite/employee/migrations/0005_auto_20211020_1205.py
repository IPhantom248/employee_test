# Generated by Django 3.2.7 on 2021-10-20 09:05

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_auto_20211004_0246'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeetree',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='employees_foto'),
        ),
        migrations.AlterField(
            model_name='employeetree',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='employee.employeetree'),
        ),
    ]
