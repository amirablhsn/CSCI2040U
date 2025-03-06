from django import forms
from .models import Vehicle

# https://docs.djangoproject.com/en/5.1/topics/forms/modelforms/#modelform
class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields  = ["make","model","trim","body","year","price", "image",
                   "description","engine", "cylinders", "fuel", "transmission",  
                   "type", "doors", "exterior_color", "interior_color", "drivetrain"]
        # https://docs.djangoproject.com/en/5.1/ref/forms/widgets/
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