# Generated by Django 3.2.8 on 2021-10-12 18:29

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0005_auto_20211012_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeetree',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='employee.employeetree'),
        ),
    ]