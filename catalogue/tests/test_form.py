from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from ..forms import VehicleForm

class TestForm(TestCase):
    #Test valid forms
    def test_valid_form(self):
        """Unit test for creating a valid form"""
        # Creating a valid form
        form = VehicleForm(data={"make":"Kia", "model": "Seltos", "year": 2023, "trim": "LX", "body": "SUV", "price": 25000.00})
        # Ensure it is valid
        self.assertTrue(form.is_valid())

    #Test invalid forms
    def test_invalid_form(self):
        """Unit test for creating invalid form"""
        # Creating a form with miss price (required)
        form = VehicleForm(data={"make":"Kia", "model": "Seltos", "year": 2023, "trim": "LX", "body": "SUV"})
        # Ensure it is invalid
        self.assertFalse(form.is_valid())

    #Test captialization of make and model
    def test_captialized_make(self):
        """Unit test for capitalizing make in form"""
        # Form with lowercase make
        form = VehicleForm(data={"make":"kia", "model": "Seltos", "year": 2023, "trim": "LX", "body": "SUV", "price": 25000.00})
        # Ensuring valid form, and cleaned data is capitalized
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["make"], "Kia")

    def test_captialized_model(self):
        """Unit test for capitalizing model in form"""
        # Form with lower case model
        form = VehicleForm(data={"make":"Honda", "model": "civic type r", "year": 2023, "trim": "LX", "body": "Sedan", "price": 25000.00})
        # Ensuring valid form, and cleaned data is capitalized
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Civic Type R")

    #Test interger fields - year, price, cylinders, and doors
    def test_year_positive(self):
        """Unit test for positive year in form"""
        # Form with negative year
        form = VehicleForm(data={"make":"Honda", "model": "civic type r", "year": -2023, "trim": "LX", "body": "Sedan", "price": 25000.00})
        # Ensure form is invalid and raises error
        self.assertFalse(form.is_valid())
        self.assertIn("year", form.errors)
        self.assertEqual(form.errors["year"][0], "Year cannot be negative.")

    def test_price_positive(self):
        """Unit test for positive price in form"""
        # Form with negative price
        form = VehicleForm(data={"make":"Honda", "model": "civic type r", "year": 2023, "trim": "LX", "body": "Sedan", "price": -25000.00})
        # Ensure form is invalid and raises error
        self.assertFalse(form.is_valid())
        self.assertIn("price", form.errors)
        self.assertEqual(form.errors["price"][0], "Price cannot be negative.")
    
    def test_cylinders_positive(self):
        """Unit test for positive cylinder in form"""
        # Form with negative cylinder
        form = VehicleForm(data={"make":"Honda", "model": "civic type r", "year": 2023, "trim": "LX", "body": "Sedan", "price": 25000.00, "cylinders": -1})
        # Invalid form and raises correct error
        self.assertFalse(form.is_valid())
        self.assertIn("cylinders", form.errors)
        self.assertEqual(form.errors["cylinders"][0], "Cylinders must be a positive integer.")

    def test_doors_must_be_at_least_one(self):
        """Unit test for cars must have at least 1 door in form"""
        # Form with no doors
        form = VehicleForm(data={"make":"Honda", "model": "civic type r", "year": 2023, "trim": "LX", "body": "Sedan", "price": -25000.00, "doors": 0})
        # Invalid form and raises correct error
        self.assertFalse(form.is_valid())
        self.assertIn("doors", form.errors)
        self.assertEqual(form.errors["doors"][0], "Doors must be at least 1.")

   #Test image file
    def test_valid_image(self):
        """Unit test for valid image file"""
        # Form with valid image
        image = SimpleUploadedFile(name='test_image.jpg', content=open("catalogue/tests/media/sample1.png", 'rb').read(), content_type='image/jpeg')
        form = VehicleForm(data={"make":"Honda", "model": "civic type r", "year": 2023, "trim": "LX", "body": "Sedan", "price": 25000.00},
                           files={"image":image})
        # Ensure form is valid
        self.assertTrue(form.is_valid())
   
    def test_invalid_image(self):
        """Unit test for form with invalid image file"""
        # Form with pdf file
        image = SimpleUploadedFile(name='test_image.pdf', content=open("catalogue/tests/media/sample1.png", 'rb').read(), content_type='image/jpeg')

        form = VehicleForm(
            data={"make": "Honda", "model": "Civic Type R", "year": 2023, "trim": "LX", "body": "Sedan", "price": 25000.00},
            files={"image": image}
        )
        # Ensure form is invalid with correct error
        self.assertFalse(form.is_valid())
        self.assertIn("image", form.errors)
        self.assertIn("Only JPG, JPEG, PNG, and WEBP formats are allowed.", form.errors["image"])


