from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
# Create your models here.

# Vehicle model with details as fields 
class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True, null=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    type = models.CharField(max_length=50, blank=True, null=True)
    year = models.IntegerField(validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])  
    engine = models.CharField(max_length=100, blank=True, null=True)
    cylinders = models.IntegerField(blank=True, null=True)
    fuel = models.CharField(max_length=50, blank=True, null=True)
    transmission = models.CharField(max_length=50, blank=True, null=True)
    trim = models.CharField(max_length=50)
    body = models.CharField(max_length=50, default="")
    doors = models.IntegerField(blank=True, null=True)
    exterior_color = models.CharField(max_length=50, blank=True, null=True)
    interior_color = models.CharField(max_length=50, blank=True, null=True)
    drivetrain = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='assets/', blank=True, null=True)

# Model for user favourites
class Favourite(models.Model):
    #  many to many relationship (user can have many favourites, and vehices can be favourited by many users)
    
    # Create a relationship between Favourite and User with ForeignKey
    # Cascasde delete - if user is deleted, delete all their favourites
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Create a relationship between Favourite and Vehicle
    # Cascasde delete - if vehicle is deleted, delete all favourites with that vehicle
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    # added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        #  all user, vehicle pairs must be unique - prevents duplicate favourites
        unique_together = ("user", "vehicle") 
