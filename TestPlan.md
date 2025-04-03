# Testing Plan
## Tesing Plan Overview
Below outlines the unit, integration, and system tests to be implemented for our application. The unit tests will use clear box testing, the integration test will use translucent box testing, and the system tests will use opaque box tests.

Unit and integration tests will be implemented using Django's `TestCase`, while system tests will be performed manually in the browser.

## Unit Tests
### 1. Vehicle Model Tests
- Testing default values
  <details>
      <summary>💻 <i>Expand Code</i></summary>
  
    ```python
    def test_optional_fields(self):
        vehicle = Vehicle.objects.create(make="Toyota", model="RAV4", year=2020, price = 30000.00, trim="LE")
        self.assertIsNone(vehicle.description)
    ```  
  </details>


- Testing object creation
  <details>
      <summary>💻 <i>Expand Code</i></summary>
       
    ```python
    Vehicle.objects.create(make="Toyota",model="RAV4", year=2022,)
    def test_vehicle_created(self):
        vehicle = Vehicle.objects.get(make="Toyota", model="RAV4")
        self.assertEqual(vehicle.year, 2022)
    ```
    
  </details>


- Testing model value contraints
  <details>
    <summary>💻 <i>Expand Code</i></summary>
    
  ```python
   def test_price_positive(self):
      vehicle = Vehicle.objects.create(make="Toyota", model="RAV4", year=2020, price =-30000.00, trim="LE")
      with self.assertRaises(ValidationError):
          vehicle.full_clean()
  
   def test_year_positive(self):
      vehicle = Vehicle.objects.create(make="Toyota", model="RAV4", year=-1999, price=30000.00, trim="LE")
      with self.assertRaises(ValidationError):
          vehicle.full_clean()
    ```
  </details>

  - Other Value Contraints to test:
    - Number of cylinders,  number of doors
    - Fuel (Gas, diesel, electric)
    - Transmission (Manual Automatic)
    - Drivetrain (AWD, RWD, 4WD, FWD)
      
### 2. Vehicle Form Tests
  - Testing valid/invalid form (required vs.optional fields)
    <details>
      <summary>💻 <i>Expand Code</i></summary>
      
      ```python
      def test_valid_form(self):
          form = VehicleForm(data={"make":"Kia", "model": "Seltos", "year": 2023, "trim": "LX", "body": "SUV", "price": 25000.00})
          self.assertTrue(form.is_valid())
  
      def test_invalid_form(self):
          form = VehicleForm(data={"make":"Kia", "model": "Seltos", "year": 2023, "trim": "LX", "body": "SUV"})
          self.assertFalse(form.is_valid())
      ```
      
    </details>
  - Testing form value constraints
    <details>
      <summary>💻 <i>Expand Code</i></summary>
      
      ```python
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
      ```
    </details>
    
    - Other Value Contraints to test:
      - Number of cylinders,  number of doors
      - Fuel (Gas, diesel, electric)
      - Transmission (Manual Automatic)
      - Drivetrain (AWD, RWD, 4WD, FWD)
        
  - Testing input cleaning functions
    <details>
      <summary>💻 <i>Expand Code</i></summary>
      
      ```python
      def test_captialized_make(self):
          form = VehicleForm(data={"make":"kia", "model": "Seltos", "year": 2023, "trim": "LX", "body": "SUV", "price": 25000.00})
          self.assertTrue(form.is_valid())
          self.assertEqual(form.cleaned_data["make"], "Kia")
  
      def test_captialized_model(self):
          form = VehicleForm(data={"make":"Honda", "model": "civic type r", "year": 2023, "trim": "LX", "body": "Sedan", "price": 25000.00})
          self.assertTrue(form.is_valid())
          self.assertEqual(form.cleaned_data["model"], "Civic Type R")
      ```
    </details>
  - Testing valid/invalid file types
     <details>
      <summary>💻 <i>Expand Test Code</i></summary>
  
       ```python
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
      ```
    </details>
### 3. User Model Tests
 - Testing user object creation
   <details>
    <summary>💻 <i>Expand Code</i></summary>

      ```python
      def test_registration(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "password",
            "password2": "password"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(username="newuser").exists())
      ```
   </details>
 - Testing user value constraints (unique username, email)
   <details>
    <summary>💻 <i>Expand Code</i></summary>

     ```python
        def test_existing_user(self):
          response = self.client.post(reverse("register"), {
              "username": "user",
              "email": "newuser@example.com",
              "password1": "password",
              "password2": "password"
          })
          self.assertEqual(response.status_code, 200)
          self.assertContains(response, "Username already exists.")
     
       def test_email_used(self): 
          response = self.client.post(reverse("register"), {
              "username": "newuser1",
              "email": "user@example.com",
              "password1": "password",
              "password2": "password"
          })
          self.assertEqual(response.status_code, 200)
          self.assertContains(response, "Email already used.")
    
       def test_mismatched_password(self):
          response = self.client.post(reverse("register"), {
              "username": "newuser2",
              "email": "newuser@example.com",
              "password1": "password",
              "password2": "password1"
          })
          self.assertEqual(response.status_code, 200)
          self.assertContains(response, "Password mismatch.")
  
         def test_missing_field(self):
          response = self.client.post(reverse("register"), {
              "username": "",
              "email": "",
              "password1": "",
              "password2": ""
          })
          self.assertEqual(response.status_code, 200)
          self.assertContains(response, "Missing field.")
  
       def test_invalid_email(self):
          response = self.client.post(reverse("register"), {
              "username": "newuser3",
              "email": "invalid_email",
              "password1": "password",
              "password2": "password"
          })
          self.assertEqual(response.status_code, 200)
          self.assertContains(response, "Invalid Email.")
  </details>
  
### 4. New User Form
  - Test valid/invalid forms (empty fields)
  - Test valid/invalid emails
  - Test password mismatch

 

## Integration Tests
1. Creating and adding a new vehicle to the database

2. Editing an existing vehicle and updating the database

3. Deleting an existing vehicle and removing it from the database

4. Searching for a vehicle

5. Filtering by criteria

6. Creating a new user and adding them to the database

7. Giving a user admin permissions

## System Tests
1. Visiting the home page and populating it with vehicles from the database

2. Clicking on vehicles verifying the details page loads, and displays the correct information

3. Typing a query into the search bar, verifying that the correct vehicles are fetched and displayed

4. Selecting a filter and verigying that the correct vehicles are filtered and displayed

5. Navigating to the vehicle form by clicking the "Add" button, filling in fields, submitting and checking that the new car and its details are displayed in the catalogue

6. Navigating to an existing vehicle page, clicking on the "Edit" button, updating the form, and confirming that the new details are displayed.

7. Navigating to an existing vehicle page, clicking on "Delete", clicking on the "Confirm" button and ensuring the vehicle no longer appears in the catalogue.

8. Clicking the "Sign Up" button, filling out the new user form, and confirming the user is created, and can login/logout.