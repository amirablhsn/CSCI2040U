import csv
import re
from catalogue.models import Vehicle

input_file = 'vehicles_dataset.csv'
output_file = 'vehicle_dataset_formatted.csv'

def format():
    year_regex = r'^\d{4}\s'
    with open(input_file, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    for row in rows:
        if row:
            row[0] = re.sub(year_regex, '', row[0]) 

    with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)


def import_csv():
    print("Inserting into database..")
    with open(output_file, newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Handle missing fields
            cylinders = int(row['cylinders']) if row['cylinders'].isdigit() else 4
            price = round(float(row['price']) if row['price'].replace('.', '', 1).isdigit() else 0.00, 2)
            mileage = int(row['mileage']) if row['mileage'].isdigit() else 0
            doors = int(row['doors']) if row['doors'].isdigit() else 4
            
            Vehicle.objects.create(
                name=row['name'],
                description=row['description'],
                make=row['make'],
                model=row['model'],
                type=row['type'],
                year=row['year'],
                price=price,
                engine=row['engine'],
                cylinders=cylinders,
                fuel=row['fuel'],
                mileage=mileage,
                transmission=row['transmission'],
                trim=row['trim'],
                body=row['body'],
                doors=doors,
                exterior_color=row['exterior_color'],
                interior_color=row['interior_color'],
                drivetrain=row['drivetrain'],
            )
    print("Imported CSV Data")
    
if __name__ == "__main__":
    import_csv()