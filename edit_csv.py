import csv
import re

input_file = 'vehicles_dataset.csv'
output_file = 'vehicle_dataset_edited.csv'

def edit_csv():
    print("Reading CSV file...")
    with open(input_file, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        # Store all rows and headers
        headers = reader.fieldnames
        rows = list(reader)
    
    print(f"Editing {len(rows)} records...")
    for row in rows:
        # Remove year prefix from description (similar to your format function)
        if 'description' in row and row['description']:
            year_regex = r'^\d{4}\s'
            row['description'] = re.sub(year_regex, '', row['description'])
        
        # Standardize values
        if 'cylinders' in row:
            row['cylinders'] = int(row['cylinders']) if row['cylinders'].isdigit() else 4
        
        if 'price' in row:
            try:
                row['price'] = round(float(row['price'].replace(',', '')), 2)
            except (ValueError, AttributeError):
                row['price'] = 0.00
        
        if 'doors' in row:
            row['doors'] = int(row['doors']) if row['doors'].isdigit() else 4
            
        # You can add more transformations here
        
        # Example: Convert make and model to uppercase
        if 'make' in row:
            row['make'] = row['make'].upper()
        if 'model' in row:
            row['model'] = row['model'].upper()
            
        # Example: Standardize fuel type
        if 'fuel' in row and row['fuel']:
            fuel_lower = row['fuel'].lower()
            if 'gas' in fuel_lower or 'gasoline' in fuel_lower:
                row['fuel'] = 'Gasoline'
            elif 'diesel' in fuel_lower:
                row['fuel'] = 'Diesel'
            elif 'electric' in fuel_lower:
                row['fuel'] = 'Electric'
            elif 'hybrid' in fuel_lower:
                row['fuel'] = 'Hybrid'
    
    print("Writing edited data to CSV...")
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"CSV editing complete. Saved to {output_file}")

if __name__ == "__main__":
    edit_csv()
