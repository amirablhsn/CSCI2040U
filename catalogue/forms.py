from django import forms
from django.core.exceptions import ValidationError
from .models import Vehicle

# https://docs.djangoproject.com/en/5.1/topics/forms/modelforms/#modelform
class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields  = ["make","model","trim","body","year","price", "image",
                   "description","engine", "cylinders", "fuel", "transmission",  
                   "type", "doors", "exterior_color", "interior_color", "drivetrain", "image"]
        # https://docs.djangoproject.com/en/5.1/ref/forms/widgets/
        # Adds bootstrap to form inputs
        widgets = {
            "make": forms.TextInput(attrs={"class": "form-control"}),
            "model": forms.TextInput(attrs={"class": "form-control"}),
            "type": forms.TextInput(attrs={"class": "form-control"}),
            "year": forms.NumberInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "engine": forms.TextInput(attrs={"class": "form-control"}),
            "cylinders": forms.NumberInput(attrs={"class": "form-control"}),
            "fuel": forms.TextInput(attrs={"class": "form-control"}),
            "transmission": forms.TextInput(attrs={"class": "form-control"}),
            "trim": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.TextInput(attrs={"class": "form-control"}),
            "doors": forms.NumberInput(attrs={"class": "form-control"}),
            "exterior_color": forms.TextInput(attrs={"class": "form-control"}),
            "interior_color": forms.TextInput(attrs={"class": "form-control"}),
            "drivetrain": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_make(self):
        """Ensure make is capitialized"""
        make = self.cleaned_data.get("make")
        return make.title() if make else make
    
    def clean_model(self):
        """Ensure model is capitialized"""
        model = self.cleaned_data.get("model")
        return model.title() if model else model
    
    def clean_price(self):
        """Ensure price is positive number"""
        price = self.cleaned_data.get("price")
        if price < 0:
            raise ValidationError("Price cannot be negative.")
        return price
    
    def clean_year(self):
        """Ensure year is positive number"""
        year = self.cleaned_data.get("year")
        if year < 0:
            raise ValidationError("Year cannot be negative.")
        return year
    
    def clean_image(self):
        """Ensure image is an image file"""
        image = self.cleaned_data.get("image")
        if image:
            if not image.name.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                raise ValidationError("Only JPG, JPEG, PNG, and WEBP formats are allowed.")
        return image
    
    def clean_cylinders(self):
        """Ensure number of cyclinders is positive"""
        cylinders = self.cleaned_data.get("cylinders")
        if cylinders is not None and cylinders < 0:
            raise ValidationError("Cylinders must be a positive integer.")
        return cylinders
    
    def clean_doors(self):
        """Ensure doors is at least 1"""
        doors = self.cleaned_data.get("doors")
        if doors is not None and doors < 1:
            raise ValidationError("Doors must be at least 1.")
        return doors