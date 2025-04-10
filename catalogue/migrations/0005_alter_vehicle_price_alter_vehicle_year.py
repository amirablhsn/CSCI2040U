# Generated by Django 5.1.6 on 2025-03-14 18:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0004_remove_vehicle_mileage_remove_vehicle_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
