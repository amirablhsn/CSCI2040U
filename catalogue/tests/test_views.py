from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Vehicle
from ..models import Favourite
#Tests for search, filter, and detail views
class VehicleViewTests(TestCase):
    def setUp(self):
        """Creating database entries to search, filter, and get details from"""
        self.vehicle1 = Vehicle.objects.create(make="Toyota", model="Corolla", year=2021, trim="LE", body="Sedan", price=25000)
        self.vehicle2 = Vehicle.objects.create(make="Honda", model="Accord", year=2022, trim="LX", body="Sedan", price=30000)
        self.vehicle3 = Vehicle.objects.create(make="Toyota", model="RAV4", year=2023, trim="LE",body="SUV", price=35000)

        # Create a user for testing favourites
        self.user = User.objects.create_user(username="user", password="password")
    
    def test_search_result(self):
        """Integration Test for searching with results found"""
        # Send a GET request to with "Toyota" query
        response = self.client.get(reverse("search") + "?catalogue-search=Toyota")

        # Renders the search page with results
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search.html")

        # Result page includes "Toyota", but not "Honda"
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Honda")

    def test_search_no_results(self):
        """Integration test for query with no results"""

        # Send get request with "Kia" query
        response = self.client.get(reverse("search") + "?catalogue-search=Kia")

        # Render the search page with no results found
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search.html")
        self.assertEqual(len(response.context["vehicles"]), 0)
        self.assertContains(response, 'No results found for "Kia"')

    def test_search_no_query(self):
        """Integration test for with empty query, should return response without fitlering any vehicles"""
        # Get request with query
        response = self.client.get(reverse("search"))
        
        # Render the search page with all 3 vehicles, non filtered
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search.html")
        self.assertEqual(len(response.context["vehicles"]), 3)


    def test_filter_make(self):
        """Integration test for filtering by make"""
        # Filter out anything not "Honda"
        response = self.client.get(reverse("filter") + "?make=Honda")

        # Render page that contain Honda Accord, but not Toyato Corolla/RAV4
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Honda Accord")
        self.assertNotContains(response, "Toyota Corolla")
        self.assertNotContains(response, "Toyota RAV4")

    def test_filter_year(self):
        """Integration test for filtering by year"""
        # Filter for cars in 2022 and 2023
        response = self.client.get(reverse("filter") + "?year_min=2022&year_max=2023")
        
        # Renders page with RAV4 (2023) and Accord (2022), but not Corolla (2021)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota RAV4")
        self.assertContains(response, "Honda Accord")
        self.assertNotContains(response, "Toyota Corolla")

    def test_filter_price(self):
        """Integration test for filtering by price"""
        # Filter cars with prices 25000-32000
        response = self.client.get(reverse("filter") + "?price_min=25000&price_max=32000")

        # Renders page with Toyota Corolla ($25000) and Accord($30000) but not RAV4 ($35000)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota Corolla")
        self.assertContains(response, "Honda Accord")
        self.assertNotContains(response, "Toyota RAV4")

    def test_filter_combo(self):
        """Integration test for combining filters"""
        # Fiilter by make and price 
        response = self.client.get(reverse("filter") + "?make=Toyota&price_max=30000")

        # Renders page with Corolla ($25000) but not RAV4 ($35000) & not Honda
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota Corolla")
        self.assertNotContains(response, "Toyota RAV4")
        self.assertNotContains(response, "Honda Accord")
    
    def test_details_valid(self):
        """Integration test for getting detail of a valid vehicle id"""
        # Getting details for Toyota Corolla
        response = self.client.get(reverse("details", args=[self.vehicle1.id]))

        # Ensure detail page renders with correct data
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "details.html")
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Corolla")
        self.assertContains(response, "2021")
        self.assertContains(response, "LE")
        self.assertContains(response, "Sedan")
        self.assertContains(response, "25,000")
        
        # Ensure default image is used
        self.assertContains(response, "/media/assets/sample2.png")

    def test_details_invalid_vehicle(self):
        """Integration test for getting details of invalid vehicle id"""
        invalid_id = 9999
        # Sending request with invalid id, results in 404 error
        response = self.client.get(reverse("details", args=[invalid_id]))
        self.assertEqual(response.status_code, 404)


    def test_favourite_requires_login(self):
        """Integration test for guest redirected when accessing favourites"""
        # Send request to favourite vehicle
        url = reverse("toggle_favourite", args=[self.vehicle1.id])
        response = self.client.get(url)
        
        # Redirects to login page
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/users/login"))

    def test_toggle_favourite(self):
        """Integration test for toggling favourite vehicle"""
        self.client.login(username="user", password="password")

        url = reverse("toggle_favourite", args=[self.vehicle1.id])
        referer = reverse("details", args=[self.vehicle1.id])

        # First toggle - add to favourites
        response = self.client.get(url, follow=True,  HTTP_REFERER=referer)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Favourite.objects.filter(user=self.user, vehicle=self.vehicle1).exists())

        # Second toggle - remove from favourites
        response = self.client.get(url, follow=True,HTTP_REFERER=referer)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Favourite.objects.filter(user=self.user, vehicle=self.vehicle1).exists())
