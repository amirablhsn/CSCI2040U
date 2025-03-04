from django.db import models
# Create your models here.

class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True, null=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    engine = models.CharField(max_length=100, blank=True, null=True)
    cylinders = models.IntegerField(blank=True, null=True)
    fuel = models.CharField(max_length=50, blank=True, null=True)
    transmission = models.CharField(max_length=50, blank=True, null=True)
    trim = models.CharField(max_length=50)
    body = models.CharField(max_length=50, blank=True, null=True)
    doors = models.IntegerField(blank=True, null=True)
    exterior_color = models.CharField(max_length=50, blank=True, null=True)
    interior_color = models.CharField(max_length=50, blank=True, null=True)
    drivetrain = models.CharField(max_length=50, blank=True, null=True)