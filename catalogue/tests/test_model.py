from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Vehicle

# Tests for Vehicle Model
class TestVehicle(TestCase):
    # Creates a tests object
    def setUp(self):
        Vehicle.objects.create(
            make="Toyota",
            model="RAV4",
            year=2022,
            price=30000.00,
            trim="LE",
            body="SUV",
            fuel="gas",
            transmission="Automatic"
        )
    
    # Tests if vehicle is created and saved
    def test_vehicle_created(self):
        vehicle = Vehicle.objects.get(make="Toyota", model="RAV4")
        self.assertEqual(vehicle.year, 2022)
        self.assertEqual(vehicle.price, 30000.00)
        self.assertEqual(vehicle.trim, "LE")
        self.assertEqual(vehicle.body, "SUV")
        self.assertEqual(vehicle.fuel, "gas")
        self.assertEqual(vehicle.transmission, "Automatic")

    # Tests optional fields
    def test_optional_fields(self):
        vehicle = Vehicle.objects.create(make="Toyota", model="RAV4", year=2020, price = 30000.00, trim="LE")
        self.assertIsNone(vehicle.description)
        self.assertIsNone(vehicle.engine)
        self.assertIsNone(vehicle.cylinders)
        self.assertIsNone(vehicle.fuel)
        self.assertIsNone(vehicle.transmission)
        self.assertIsNone(vehicle.doors)
        self.assertIsNone(vehicle.exterior_color)
        self.assertIsNone(vehicle.interior_color)
        self.assertIsNone(vehicle.drivetrain)
        self.assertFalse(bool(vehicle.image))

    # Tests price is positive number
    def test_price_positive(self):
        vehicle = Vehicle.objects.create(make="Toyota", model="RAV4", year=2020, price =-30000.00, trim="LE")
        with self.assertRaises(ValidationError):
            vehicle.full_clean()

    # Tests year is positive numeber
    def test_year_positive(self):
        vehicle = Vehicle.objects.create(make="Toyota", model="RAV4", year=-1999, price=30000.00, trim="LE")
        with self.assertRaises(ValidationError):
            vehicle.full_clean()
