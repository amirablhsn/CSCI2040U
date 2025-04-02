from django.test import TestCase
from django.urls import reverse
from ..models import Vehicle
from django.contrib.auth.models import User

# Integration Tests for admin features - add, edit, delete
class VehicleAdminViewTests(TestCase):
    def setUp(self):
        """Sets the mock test client to admin to run add, edit, delete functions"""
        self.user = User.objects.create_user(username="admin", password="password", is_staff=True)
        self.client.login(username="admin", password="password")

    def test_add_view_valid(self):
        """Integration test of the add feature with valid inputs. After adding a vehcile client should be redirected to the details page of that vehicle"""
        # Send POST request to add with vehicle details, returns a response
        response = self.client.post(reverse("add"), {"make":"Kia", "model": "Seltos", "year": 2023, "trim": "LX", "body": "SUV", "price": 25000.00})
        
        # Redirect status code, client should be redireted to the details pages after success
        self.assertEqual(response.status_code, 302)

        # Ensure added, mock database should have 1 entry now
        self.assertEqual(Vehicle.objects.count(), 1)
        # Get the added vehicle from the database and ensure client is redirected to the correct vehicle page (based on vehicle id)
        vehicle = Vehicle.objects.first()        
        self.assertRedirects(response, reverse("details", args=[vehicle.id]))
        
        # Check vehicle data to ensure it matches input
        self.assertEqual(vehicle.make, "Kia")
        self.assertEqual(vehicle.model, "Seltos")
        self.assertEqual(vehicle.year, 2023)
        self.assertEqual(vehicle.trim, "LX")
        self.assertEqual(vehicle.body, "SUV")
        self.assertEqual(vehicle.price, 25000.00)
       
        # Check optional fields required 
        self.assertIsNone(vehicle.engine)
        self.assertIsNone(vehicle.cylinders)
        self.assertIsNone(vehicle.fuel)
        self.assertIsNone(vehicle.transmission)
        self.assertIsNone(vehicle.doors)
        self.assertIsNone(vehicle.exterior_color)
        self.assertIsNone(vehicle.interior_color)
        self.assertIsNone(vehicle.drivetrain)
        self.assertFalse(bool(vehicle.image))


    def test_add_view_invalid(self):
        """Integration test of the add feature with invalid inputs. Should re-render the page instead of re-directing"""
        # Sending a request to add a vehicle with missing required fields (model, year)
        response = self.client.post(reverse("add"), {
            "model": "Seltos",
            "year": 2023,
            "trim": "LX",
            "body": "SUV"
        })

        # Ensure nothing was added to the database
        self.assertEqual(Vehicle.objects.count(), 0)

        # Ensure the client is not redirected, instead theform is re-rendered (status code 200), and client is on "add" page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add.html")
        
    def test_edit_view_valid(self):
        """Integration Test for the edit feature with valid inputs. Should redirect the client to the details page and update the database"""
        # Create a vehicle, and send a request to edit the vehicle with new data
        vehicle = Vehicle.objects.create(make="Kia", model= "Seltos", year=2023, trim="LX", body="SUV", price=25000.00)
        
        # Ensure the vehicle exists to edit
        self.assertEqual(Vehicle.objects.count(), 1)
        self.assertTrue(Vehicle.objects.filter(id=vehicle.id).exists())
        
        #Send POST request to edit to year, trim, body
        response = self.client.post(reverse("edit", args=[vehicle.id]), {
            "make":"Kia",
            "model": "Seltos",
            "year": 2020,
            "trim": "LE",
            "body": "Sedan",
            "price": 25000.00,
        })

        # Ensure the client is redirected to the details pages
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("details", args=[vehicle.id]))

        # Retrieve the updated vehicle from database and check if edited fields have been updated
        vehicle.refresh_from_db()
        self.assertEqual(vehicle.make, "Kia")
        self.assertEqual(vehicle.model, "Seltos")
        self.assertEqual(vehicle.year, 2020)
        self.assertEqual(vehicle.trim, "LE")
        self.assertEqual(vehicle.body, "Sedan")
        self.assertEqual(vehicle.price, 25000.00)

    def test_edit_view_invalid_data(self):
        """Integration Test for the edit feature with invalid inputs. Should re-render the edit page, and keep database entry the same"""
        # Create a vehicle, and send a request to edit the vehicle with missing field
        vehicle = Vehicle.objects.create(make="Kia", model= "Seltos", year=2023, trim="LX", body="SUV", price=25000.00)
        self.assertEqual(Vehicle.objects.count(), 1)
        self.assertTrue(Vehicle.objects.filter(id=vehicle.id).exists())

        # Sends POST request to edit vehicle with vehicle make missing
        response = self.client.post(reverse("edit", args=[vehicle.id]), {
            "model": "Seltos",
            "year": 2020,
            "trim": "LE",
            "body": "Sedan",
            "price": 25000.00,
        })

        # Ensure the client re-renders the edit page, and not redirected to details
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit.html")

        # Retrieve the updated vehicle from database and ensure it has not been updated
        vehicle.refresh_from_db()
        self.assertEqual(vehicle.make, "Kia")
        self.assertEqual(vehicle.model, "Seltos")
        self.assertEqual(vehicle.year, 2023)
        self.assertEqual(vehicle.trim, "LX")
        self.assertEqual(vehicle.body, "SUV")
        self.assertEqual(vehicle.price, 25000.00)

    def test_edit_invalid_vehicle(self):
        """Intefration test for editing vehicle with invalid id"""
        invalid_id = 9999
        # Sending request with invalid id, results in 404 error
        response = self.client.get(reverse("edit", args=[invalid_id]))
        self.assertEqual(response.status_code, 404)


    def test_delete_vehicle(self):
        """Integration test for deleting vehicles. Should remvoe from database adn redirect to home page"""
        vehicle = Vehicle.objects.create(make="Kia", model= "Seltos", year=2023, trim="LX", body="SUV", price=25000.00)
        self.assertEqual(Vehicle.objects.count(), 1)
        self.assertTrue(Vehicle.objects.filter(id=vehicle.id).exists())

        # Send a POST request to delete the vehicle by id
        response = self.client.post(reverse('delete', args=[vehicle.id]))

        # Ensure the client is redirected to the home page 
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

        # Ensure the vehcile is deleted from the database
        self.assertEqual(Vehicle.objects.count(), 0)
        self.assertFalse(Vehicle.objects.filter(id=vehicle.id).exists())
    
    def test_delete_invalid(self):
        """Integration test for deleting vehicle with invalid id"""
        invalid_id = 9999
        # Sending request with invalid id, results in 404 error
        response = self.client.get(reverse("delete", args=[invalid_id]))
        self.assertEqual(response.status_code, 404)

    