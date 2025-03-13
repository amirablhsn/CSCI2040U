from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from ..forms import VehicleForm

class TestForm(TestCase):
    #Test valid forms
    def test_valid_form(self):
        form = VehicleForm(data={"make":"Kia", "model": "Seltos", "year": 2023, "trim": "LX", "body": "SUV", "price": 25000.00})
        self.assertTrue(form.is_valid())

    #Test invalid forms
    def test_invalid_form(self):
        form = VehicleForm(data={"make":"Kia", "model": "Seltos", "year": 2023, "trim": "LX", "body": "SUV"})
        self.assertFalse(form.is_valid())

    #Test captialization of make and model
    def test_captialized_make(self):
        form = VehicleForm(data={"make":"kia", "model": "Seltos", "year": 2023, "trim": "LX", "body": "SUV", "price": 25000.00})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["make"], "Kia")

    def test_captialized_model(self):
        form = VehicleForm(data={"make":"Honda", "model": "civic type r", "year": 2023, "trim": "LX", "body": "Sedan", "price": 25000.00})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Civic Type R")

    #Test interger fields - year, price, cylinders, and doors
    def test_year_positive(self):
        form = VehicleForm(data={"make":"Honda", "model": "civic type r", "year": -2023, "trim": "LX", "body": "Sedan", "price": 25000.00})
        self.assertFalse(form.is_valid())
        self.assertIn("year", form.errors)
        self.assertEqual(form.errors["year"][0], "Year cannot be negative.")

    def test_price_positive(self):
        form = VehicleForm(data={"make":"Honda", "model": "civic type r", "year": 2023, "trim": "LX", "body": "Sedan", "price": -25000.00})
        self.assertFalse(form.is_valid())
        self.assertIn("price", form.errors)
        self.assertEqual(form.errors["price"][0], "Price cannot be negative.")
    
    def test_cylinders_positive(self):
        form = VehicleForm(data={"make":"Honda", "model": "civic type r", "year": 2023, "trim": "LX", "body": "Sedan", "price": -25000.00, "cylinders": -1})
        self.assertFalse(form.is_valid())
        self.assertIn("cylinders", form.errors)
        self.assertEqual(form.errors["cylinders"][0], "Cylinders must be a positive integer.")

    def test_doors_must_be_at_least_one(self):
        form = VehicleForm(data={"make":"Honda", "model": "civic type r", "year": 2023, "trim": "LX", "body": "Sedan", "price": -25000.00, "doors": 0})
        self.assertFalse(form.is_valid())
        self.assertIn("doors", form.errors)
        self.assertEqual(form.errors["doors"][0], "Doors must be at least 1.")

   #Test image file
    def test_valid_image(self):
        image = SimpleUploadedFile(name='test_image.jpg', content=open("catalogue/tests/media/sample1.png", 'rb').read(), content_type='image/jpeg')
        form = VehicleForm(data={"make":"Honda", "model": "civic type r", "year": 2023, "trim": "LX", "body": "Sedan", "price": 25000.00},
                           files={"image":image})
        self.assertTrue(form.is_valid())
   
    def test_invalid_image(self):
        image = SimpleUploadedFile("test.txt", b"file_content", content_type="text/plain")
        form = VehicleForm(data={"make":"Honda", "model": "civic type r", "year": 2023, "trim": "LX", "body": "Sedan", "price": 25000.00},
                           files={"image":image})
        self.assertFalse(form.is_valid())

