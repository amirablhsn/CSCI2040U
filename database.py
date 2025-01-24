import csv
import os

csv_file = "./catalog/data/items.csv"
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