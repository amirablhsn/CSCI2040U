from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re


class LoginForm(forms.Form):
    """Login form, requires username and password"""
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        """Used to add bootstrap styles to the form fields"""
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields["username"].widget.attrs.update({
        "class": "form-control",
        "placeholder": "Username"
        })
        self.fields["password"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Password"
        })
    
class RegisterForm(UserCreationForm):
    """Registration form for new users"""
    class Meta:
        model = User
        fields = ["username","email","password1","password2"]
        
        email = forms.EmailField(required=True)

        # Add bootstrap class to form fields
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            }
    
    def clean_email(self):
        """Ensures valid email input"""
        email = self.cleaned_data.get("email")
        
        # Error if empty email field
        if not email:
            raise ValidationError("Missing Field")
        
        # Error if invalid email 
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError("Enter a valid email address.")
        
        # Error if email already used
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already used.")
        
        return email

    def clean_username(self):
        """Ensures valid username input"""

        username = self.cleaned_data["username"]
        # Error if empty username 
        if not username:
            raise ValidationError("Missing field.")
        
        # Error if username already used.
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")
        return username

    def clean(self):
        """Handles password field"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Error if either password inputs are missing
        if not password1 or not password2:
            self.add_error(None, "Missing field.")
        
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # Adding bootstrap class to password fields
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})