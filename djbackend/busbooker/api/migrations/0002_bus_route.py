# Generated by Django 5.1.2 on 2024-10-29 03:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='route',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buses', to='api.route'),
        ),
    ]
