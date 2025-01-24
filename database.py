import csv
import os

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

init_db()

# Returns true if name and desc are non-empty strings
def validate_input(name, description):
    return name.strip() != "" and description.strip() != ""

# Reads csv file, returns database entires in a list of dicts
def fetch_all():
    with open(csv_file, mode="r", newline="") as data_file:
        reader = csv.DictReader(data_file)
        return list(reader)

def add(name, description):
    if not validate_input(name, description):
        return
    
    data = fetch_all()

    # Auto increments id
    if len(data) == 0:
        id = 1
    else: 
        id = int(data[-1]["ID"]) + 1
    
    # appends new data entry
    with open(csv_file, mode="a", newline="") as data_file:
        writer = csv.writer(data_file)
        writer.writerow([id, name, description])

# deletes data entry by id, returns true if successful
def delete(id):
    data = fetch_all()
    success = False

    for entry in data:
        if entry["ID"] == str(id):
            data.remove(entry)
            success = True
            break
    
    # Only updates file if entry is found and removed
    if success:
        with open(csv_file, mode="w", newline="") as data_file:
            writer = csv.DictWriter(data_file, field_names)
            writer.writeheader()
            writer.writerows(data)

    return success