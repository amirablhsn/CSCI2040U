from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class TestUserRegistration(TestCase):
    def setUp(self):
        """Creates a register user for testing"""
        self.user = get_user_model().objects.create_user(username="user", email="user@example.com", password="TestPass123!")
    
    def test_registration(self):
        """Tests successful user registration"""
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "TestPass123!",
            "password2": "TestPass123!"
        })

        # Ensure the user is redirected and they have been added to the database
        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(username="newuser").exists())

    def test_existing_user(self):
        """Test registration attempt with a username that is already used"""

        # Request with username in use
        response = self.client.post(reverse("register"), {
            "username": "user",
            "email": "newuser@example.com",
            "password1": "TestPass123!",
            "password2": "TestPass123!"
        })

        # Re-renders the page and notifies them that username already exists
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Username already exists.")
    
    # Tests email already used
    def test_email_used(self):
        """Test registration attempt with ana email that is already used"""
 
        response = self.client.post(reverse("register"), {
            "username": "newuser1",
            "email": "user@example.com",
            "password1": "TestPass123!",
            "password2": "TestPass123!"
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email already used.")
    
    def test_mismatched_password(self):
        """Test registartion where password1 and password 2 aren't the same"""
        response = self.client.post(reverse("register"), {
            "username": "newuser2",
            "email": "newuser2@example.com",
            "password1": "TestPass123!",
            "password2": "TestPass1!"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The two password fields didn’t match.")

    # Tests differnt missing registration field inputs
    def test_missing_field(self):
        response = self.client.post(reverse("register"), {
            "username": "",
            "email": "",
            "password1": "",
            "password2": ""
        })
        self.assertEqual(response.status_code, 200)
   
    def test_missing_field_user(self):
        response = self.client.post(reverse("register"), {
            "username": "",
            "email": "newuser3@example.com",
            "password1": "TestPass123!",
            "password2": "TestPass123!"
        })
        self.assertEqual(response.status_code, 200)
    
    def test_missing_field_email(self):
        response = self.client.post(reverse("register"), {
            "username": "user4",
            "email": "",
            "password1": "TestPass123!",
            "password2": "TestPass123!"
        })
        self.assertEqual(response.status_code, 200)
    
    def test_missing_field_password1(self):
        response = self.client.post(reverse("register"), {
            "username": "user5",
            "email": "newuser5@example.com",
            "password1": "",
            "password2": "TestPass123!"
        })
        self.assertEqual(response.status_code, 200)

    def test_missing_field_password2(self):
        response = self.client.post(reverse("register"), {
            "username": "user6",
            "email": "newuser6@example.com",
            "password1": "TestPass123!",
            "password2": ""
        })
        self.assertEqual(response.status_code, 200)


    def test_invalid_email(self):
        """Test handling invalid email format"""
        response = self.client.post(reverse("register"), {
            "username": "newuser7",
            "email": "invalid_email",
            "password1": "TestPass123!",
            "password2": "TestPass123!"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid email address.")