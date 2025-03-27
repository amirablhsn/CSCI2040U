from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class TestUserRegistration(TestCase):
    def setUp(self):
            self.user = get_user_model().objects.create_user(username="user", email="user@example.com", password="password123")
    
    # Tests successful user registration
    def test_registration(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "password",
            "password2": "password"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(username="newuser").exists())

    # Test username already exists
    def test_existing_user(self):
        response = self.client.post(reverse("register"), {
            "username": "user",
            "email": "newuser@example.com",
            "password1": "password",
            "password2": "password"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Username already exists.")
    
    # Tests email already used
    def test_email_used(self): 
        response = self.client.post(reverse("register"), {
            "username": "newuser1",
            "email": "user@example.com",
            "password1": "password",
            "password2": "password"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email already used.")
    
    # Test passwords confimration mismatch
    def test_mismatched_password(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser2",
            "email": "newuser@example.com",
            "password1": "password",
            "password2": "password1"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Password mismatch.")

    # Test missing field input
    def test_missing_field(self):
        response = self.client.post(reverse("register"), {
            "username": "",
            "email": "",
            "password1": "",
            "password2": ""
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Missing field.")

    # Test invalid email format
    def test_invalid_email(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser3",
            "email": "invalid_email",
            "password1": "password",
            "password2": "password"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid Email.")