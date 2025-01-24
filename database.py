import csv
import os
import sys

csv_file = "./items.csv"
field_names = ["ID", "Name", "Description"]

def generate_dummy_data(entries=5):
    data = []
    for i in range(1, entries + 1):
        data.append({"ID": i, "Name": "Item " + str(i), "Description": "Desc " + str(i)})
    return data

def init_db(dummy_data=True):
    if not os.path.isfile(csv_file) or os.path.getsize(csv_file) == 0:
        with open(csv_file, mode="w", newline="") as data_file:
            writer = csv.DictWriter(data_file, field_names)
            writer.writeheader()
            if dummy_data:
                writer.writerows(generate_dummy_data())
            print("Database initialized")

def validate_input(name, description):
    return name.strip() != "" and description.strip() != ""

def fetch_all():
    with open(csv_file, mode="r", newline="") as data_file:
        reader = csv.DictReader(data_file)
        return list(reader)

def add(name, description):
    if not validate_input(name, description):
        print("Invalid input. Name and description cannot be empty.")
        return
    
    data = fetch_all()
    id = int(data[-1]["ID"]) + 1 if data else 1
    
    with open(csv_file, mode="a", newline="") as data_file:
        writer = csv.writer(data_file)
        writer.writerow([id, name, description])
    print(f"Added item: {name}")

def delete(id):
    data = fetch_all()
    success = False
    for entry in data:
        if entry["ID"] == str(id):
            data.remove(entry)
            success = True
            break
    
    if success:
        with open(csv_file, mode="w", newline="") as data_file:
            writer = csv.DictWriter(data_file, field_names)
            writer.writeheader()
            writer.writerows(data)
        print(f"Deleted item with ID: {id}")
    else:
        print(f"No item found with ID: {id}")
    return success

def edit_data(id, new_name, new_description):
    updated = False
    temp_file = csv_file + '.tmp'
    
    if not os.path.isfile(csv_file) or os.path.getsize(csv_file) == 0:
        print("Database is missing or empty")
        return False
    
    with open(csv_file, mode='r', newline='', encoding='utf-8') as csvfile, \
        open(temp_file, mode='w', newline='', encoding='utf-8') as tempfile:
        reader = csv.reader(csvfile)
        writer = csv.writer(tempfile)
        header = next(reader)
        writer.writerow(header)
        for row in reader:
            if row[0] == str(id):
                row[1] = new_name
                row[2] = new_description
                updated = True
            writer.writerow(row)
    
    if updated:
        os.replace(temp_file, csv_file)
        print(f"Updated item with ID: {id}")
    else:
        if os.path.isfile(temp_file):
            os.remove(temp_file)
        print(f"No item found with ID: {id}")
    
    return updated

def display_items():
    items = fetch_all()
    if not items:
        print("No items in the inventory.")
        return
    
    print("\nCurrent Inventory:")
    print("-" * 40)
    for item in items:
        print(f"ID: {item['ID']}, Name: {item['Name']}")
    print("-" * 40)

def view_item_details(item_id):
    items = fetch_all()
    for item in items:
        if item['ID'] == str(item_id):
            print("\nItem Details:")
            print(f"ID: {item['ID']}")
            print(f"Name: {item['Name']}")
            print(f"Description: {item['Description']}")
            return
    print(f"No item found with ID: {item_id}")

def main_menu():
    init_db()
    while True:
        print("\n--- Inventory Management System ---")
        print("1. View All Items")
        print("2. View Item Details")
        print("3. Add New Item")
        print("4. Edit Item")
        print("5. Delete Item")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            display_items()
        elif choice == '2':
            item_id = input("Enter item ID to view details: ")
            view_item_details(item_id)
        elif choice == '3':
            name = input("Enter item name: ")
            description = input("Enter item description: ")
            add(name, description)
        elif choice == '4':
            item_id = input("Enter item ID to edit: ")
            new_name = input("Enter new name: ")
            new_description = input("Enter new description: ")
            edit_data(item_id, new_name, new_description)
        elif choice == '5':
            item_id = input("Enter item ID to delete: ")
            delete(item_id)
        elif choice == '6':
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
