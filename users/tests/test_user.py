from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.contrib.messages import get_messages
from django.urls import reverse
from catalogue.models import Favourite, Vehicle

class UserAccountTests(TestCase):
    def setUp(self):
        """Creat user and vehicle for tests"""
        self.client = Client()
        self.user = User.objects.create_user(username="user", password="password")
        self.vehicle = Vehicle.objects.create(make="Toyota", model="RAV4", year=2023, trim="LE",body="SUV", price=35000)

    def test_valid_login(self):
        """Test valid username and password"""
        # Send POST with correct username/password
        response = self.client.post(reverse("login"), {
            "username": "user",
            "password": "password"
        }, follow=True)
        
        # Redirects to home and and user is logged in
        self.assertRedirects(response, "/")
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_invalid_login(self):
        """Test invalid username/password login attempt"""
        
        # Send POST with incorrect password
        response = self.client.post(reverse("login"), {
            "username": "user",
            "password": "wrongpass"
        }, follow=True)

        # re-renders login in page, user not logged in
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_user_logout(self):
        """Test logging out user, redirects to home"""
        # Login in client, and send request to logout
        self.client.login(username="user", password="password")
        response = self.client.get(reverse("logout"), follow=True)

        # redirect to home, user is logged out
        self.assertRedirects(response, "/")
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_profile_favourites(self):
        """Test profile with favourited vehicles"""
        # Login in user and add vehicle to users favourites
        self.client.login(username="user", password="password")
        Favourite.objects.create(user=self.user, vehicle=self.vehicle)

        # Request to profile page
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")
        
        # Ensure Toyota RAV4 is included
        self.assertContains(response, "Toyota")
        self.assertContains(response, "RAV4")
