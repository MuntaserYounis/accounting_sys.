# Generated by Django 2.2.4 on 2023-07-13 23:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('the_app', '0003_remove_rental_rental_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='the_app.Car'),
        ),
        migrations.AlterField(
            model_name='rental',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='the_app.Client'),
        ),
    ]
