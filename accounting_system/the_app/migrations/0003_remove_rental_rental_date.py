# Generated by Django 2.2.4 on 2023-07-13 23:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('the_app', '0002_car_variable_cost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rental',
            name='rental_date',
        ),
    ]
