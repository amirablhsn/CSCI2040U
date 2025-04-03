from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse

from catalogue.models import Vehicle

# Test for the admin role -> users with Django staff are have "admin" privileges to add, edit, and delete 
class AdminTest(TestCase):
    def setUp(self):
        """Create regular user, admin, and vehicles for testing"""
        self.client = Client()
        self.user = User.objects.create_user(username="user", password="password")
        self.staff = User.objects.create_user(username="admin", password="password", is_staff=True)

        self.vehicle = Vehicle.objects.create(make="Kia", model= "Seltos", year=2023, trim="LX", body="SUV", price=25000.00)


    def test_request_admin(self):
        """Integration test for user requesting admin"""
        # login as user and request admin
        self.client.login(username="user", password="password")
        response = self.client.post(reverse('request_admin'))
        
        # Check if user has been given admin, and redirects them to profile page
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_staff)
        self.assertRedirects(response, reverse("profile"))

    def test_remove_admin(self):
        """Integration test for removing admin"""
        # Set user to admin and login
        self.user.is_staff = True
        self.user.save()
        self.client.login(username="user", password="password")

        # Send request to remove admin, ensure they are no longer admin and redirect to profile page
        response = self.client.post(reverse('remove_admin'))
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_staff)
        self.assertRedirects(response, reverse("profile"))

    def test_add_access(self):
        """Integration test for accessing add page"""
        url = reverse("add")

        # Guest accessing add page, redirects to home page
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/?next=/add/")

        # User accessing, redirects to home page
        self.client.login(username="user", password="password")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/?next=/add/")

        # Admin accessing renders the add page
        self.client.login(username="admin", password="password")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_edit_access(self):
        """Integration test for accessing edit page"""
        url = reverse("edit", args=[self.vehicle.id])

        # Guest accessing add page, redirects to home page
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/?next=/edit/1/")

        # User accessing, redirects to home page
        self.client.login(username="user", password="password")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/?next=/edit/1/")

        # Admin accessing renders the add pagec
        self.client.login(username="admin", password="password")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_access(self):
        """Integration test for accessing delete page"""
        url = reverse("delete", args=[self.vehicle.id])

        # Guest accessing add page, redirects to home page
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/?next=/delete/1/")

        # User accessing, redirects to home page
        self.client.login(username="user", password="password")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/?next=/delete/1/")

        # Admin accessing renders the add pagec
        self.client.login(username="admin", password="password")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)