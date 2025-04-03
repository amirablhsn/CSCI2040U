import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autosearchapp.settings")
django.setup()
from django.core.files import File
from catalogue.models import Vehicle

image_dir = "images"
def add_images():
    # Loop through all image files -> named make_model_year
    for filename in os.listdir(image_dir):
        # right split, then split by _
        car_data = filename.rsplit(".", 1)[0].split("_")

        make = car_data[0].lower()
        model = car_data[1].lower()
        year = int(car_data[2])

        try:
            # Find the car in the database
            cars = Vehicle.objects.filter(make__iexact=make, model__iexact=model, year=year)

            for car in cars:
                # Add the image for the car
                with open(os.path.join(image_dir, filename), "rb") as f:
                    car.image.save(filename, File(f), save=True)
            print(f"Image added for {car.make} {car.model} {car.year}")
        except Vehicle.DoesNotExist:
            print(f"No matching car found for {filename}")
