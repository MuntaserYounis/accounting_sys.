# Generated by Django 2.2.4 on 2023-07-13 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('the_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='variable_cost',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]