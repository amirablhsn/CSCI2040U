from django.db import models
# Create your models here.

class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    engine = models.CharField(max_length=100)
    cylinders = models.IntegerField()
    fuel = models.CharField(max_length=50)
    mileage = models.IntegerField()
    transmission = models.CharField(max_length=50)
    trim = models.CharField(max_length=50)
    body = models.CharField(max_length=50)
    doors = models.IntegerField()
    exterior_color = models.CharField(max_length=50)
    interior_color = models.CharField(max_length=50)
    drivetrain = models.CharField(max_length=50)