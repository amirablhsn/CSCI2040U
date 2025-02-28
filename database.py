import csv
import os
import sys

# Path to the CSV file that stores the items
csv_file = "./items.csv"
# Field names for the CSV (columns: ID, Name, and Description)
field_names = ["ID", "Name", "Description"]


# Function to generate dummy data (default is 5 entries)
def generate_dummy_data(entries=5):
    data = []
    # Generate a list of dictionaries for the dummy data
    for i in range(1, entries + 1):
        data.append(
            {"ID": i, "Name": "Item " + str(i), "Description": "Desc " + str(i)}
        )
    return data


# Function to initialize the database (CSV file)
def init_db(dummy_data=True):
    # If the file doesn't exist or is empty, create it
    if not os.path.isfile(csv_file) or os.path.getsize(csv_file) == 0:
        with open(csv_file, mode="w", newline="") as data_file:
            writer = csv.DictWriter(data_file, field_names)
            writer.writeheader()
            # Optionally, write dummy data to the file
            if dummy_data:
                writer.writerows(generate_dummy_data())
            print("Database initialized")


# Function to validate input: checks if the name and description are non-empty
def validate_input(name, description):
    return name.strip() != "" and description.strip() != ""


# Function to fetch all items from the CSV file
def fetch_all():
    with open(csv_file, mode="r", newline="") as data_file:
        reader = csv.DictReader(data_file)
        return list(reader)


# Function to add a new item to the database
def add(name, description):
    # If inputs are invalid (empty), do not add the item
    if not validate_input(name, description):
        print("Invalid input. Name and description cannot be empty.")
        return

    data = fetch_all()
    # Calculate the next ID for the new item (increment last ID)
    id = int(data[-1]["ID"]) + 1 if data else 1

    # Open the file in append mode to add the new item
    with open(csv_file, mode="a", newline="") as data_file:
        writer = csv.writer(data_file)
        writer.writerow([id, name, description])
    print(f"Added item: {name}")


# Function to delete an item by its ID
def delete(id):
    data = fetch_all()
    success = False
    # Iterate over the data to find and remove the item with the given ID
    for entry in data:
        if entry["ID"] == str(id):
            data.remove(entry)
            success = True
            break

    # If an item was deleted, rewrite the CSV with updated data
    if success:
        with open(csv_file, mode="w", newline="") as data_file:
            writer = csv.DictWriter(data_file, field_names)
            writer.writeheader()
            writer.writerows(data)
        print(f"Deleted item with ID: {id}")
    else:
        print(f"No item found with ID: {id}")
    return success


# Function to edit an existing item by its ID
def edit_data(id, new_name, new_description):
    updated = False
    temp_file = csv_file + ".tmp"

    # If the CSV file is missing or empty, print an error
    if not os.path.isfile(csv_file) or os.path.getsize(csv_file) == 0:
        print("Database is missing or empty")
        return False

    # Open the original CSV file and a temporary file for writing
    with open(csv_file, mode="r", newline="", encoding="utf-8") as csvfile, open(
        temp_file, mode="w", newline="", encoding="utf-8"
    ) as tempfile:
        reader = csv.reader(csvfile)
        writer = csv.writer(tempfile)
        header = next(reader)
        writer.writerow(header)
        # Iterate over each row and update the matching item
        for row in reader:
            if row[0] == str(id):
                row[1] = new_name
                row[2] = new_description
                updated = True
            writer.writerow(row)

    # If update was successful, replace the original file with the temporary one
    if updated:
        os.replace(temp_file, csv_file)
        print(f"Updated item with ID: {id}")
    else:
        # If no item was found, remove the temp file and notify the user
        if os.path.isfile(temp_file):
            os.remove(temp_file)
        print(f"No item found with ID: {id}")

    return updated


# Function to display all items in the inventory
def display_items():
    items = fetch_all()
    if not items:
        print("No items in the inventory.")
        return

    print("\nCurrent Inventory:")
    print("-" * 40)
    # Iterate and print each item in the inventory
    for item in items:
        print(f"ID: {item['ID']}, Name: {item['Name']}")
    print("-" * 40)


# Function to view details of a specific item by ID
def view_item_details(item_id):
    items = fetch_all()
    for item in items:
        if item["ID"] == str(item_id):
            print("\nItem Details:")
            print(f"ID: {item['ID']}")
            print(f"Name: {item['Name']}")
            print(f"Description: {item['Description']}")
            return
    # If the item ID is not found, notify the user
    print(f"No item found with ID: {item_id}")


# Main menu function that runs the program
def main_menu():
    init_db()  # Initialize the database (create file if it doesn't exist)
    while True:
        # Display the main menu with options
        print("\n--- Inventory Management System ---")
        print("1. View All Items")
        print("2. View Item Details")
        print("3. Add New Item")
        print("4. Edit Item")
        print("5. Delete Item")
        print("6. Exit")

        # Get the user's choice
        choice = input("Enter your choice (1-6): ")

        # Handle each choice with the corresponding function
        if choice == "1":
            display_items()
        elif choice == "2":
            item_id = input("Enter item ID to view details: ")
            view_item_details(item_id)
        elif choice == "3":
            name = input("Enter item name: ")
            description = input("Enter item description: ")
            add(name, description)
        elif choice == "4":
            item_id = input("Enter item ID to edit: ")
            new_name = input("Enter new name: ")
            new_description = input("Enter new description: ")
            edit_data(item_id, new_name, new_description)
        elif choice == "5":
            item_id = input("Enter item ID to delete: ")
            delete(item_id)
        elif choice == "6":
            print("Goodbye!")
            sys.exit(0)  # Exit the program
        else:
            print("Invalid choice. Please try again.")


# Start the program by calling the main menu function
if __name__ == "__main__":
    main_menu()
