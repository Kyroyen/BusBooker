# Generated by Django 5.1.2 on 2024-10-29 23:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_bus_managers_alter_route_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus',
            name='scheduled_date',
            field=models.DateField(default=datetime.date(2024, 10, 30)),
        ),
    ]
