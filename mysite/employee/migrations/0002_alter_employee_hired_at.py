# Generated by Django 3.2.7 on 2021-10-03 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='hired_at',
            field=models.DateField(),
        ),
    ]