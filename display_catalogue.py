import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import os

# Function to display the car catalogue
def display_car_catalogue():
    # Create the main window
    root = tk.Tk()
    root.title("Car Catalogue")

    # Add a label for the title
    title_label = tk.Label(root, text="Car Catalogue", font=("Helvetica", 24))
    title_label.pack(pady=10)

    # Folder containing car images and details (you'll need to modify this)
    car_folder = "assets/"  # Modify this to the folder where you have your PNGs
    car_details = {
        "sample1.png": {"name": "Car Model A", "description": "A powerful sports car."},
        "sample2.png": {"name": "Car Model B", "description": "An electric sedan."},
        "sample3.png": {"name": "Car Model C", "description": "A family-friendly SUV."}
        # Add more cars as needed
    }

    # Loop to display each car's image and details
    for car_image, details in car_details.items():
        frame = tk.Frame(root)
        frame.pack(pady=10)

        # Image display
        img_path = os.path.join(car_folder, car_image)
        img = Image.open(img_path)
        img = img.resize((200, 200))  # Resize image to fit window
        img_tk = ImageTk.PhotoImage(img)

        img_label = tk.Label(frame, image=img_tk)
        img_label.image = img_tk  # Keep a reference to the image to prevent garbage collection
        img_label.grid(row=0, column=0, padx=10)

        # Car details display
        name_label = tk.Label(frame, text=details["name"], font=("Helvetica", 16))
        name_label.grid(row=0, column=1, sticky="w")

        description_label = tk.Label(frame, text=details["description"], font=("Helvetica", 12), wraplength=250)
        description_label.grid(row=1, column=1, sticky="w", padx=10)

    # Start the Tkinter event loop
    root.mainloop()

# Call the function to display the catalogue
display_car_catalogue()