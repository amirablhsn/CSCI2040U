# Generated by Django 5.1.5 on 2025-03-03 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='cylinders',
            field=models.IntegerField(default=4),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='description',
            field=models.TextField(default='No description'),
        ),
    ]
