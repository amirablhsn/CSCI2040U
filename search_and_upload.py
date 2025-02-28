import os
import subprocess

# Function to search for PNG files in a directory and its subdirectories
def search_images(directory):
    png_files = []
    # Traverse directory tree
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file is a PNG image
            if file.lower().endswith('.png'):
                png_files.append(os.path.join(root, file))
    return png_files

# Function to upload the PNG files to GitHub
def upload_to_github():
    # Git commands to commit & push
    subprocess.run("git add .", shell=True)
    subprocess.run('git commit -m "Added PNG images"', shell=True)
    subprocess.run("git push origin main", shell=True)

    print("🚀 Images uploaded to GitHub!")

# Directory to search for PNG images (modify as needed)
directory = "assets"  # Update this to your folder path

# Search for PNG images
png_files = search_images(directory)

# Print out the found PNG files
if png_files:
    print("Found the following PNG files:")
    for file in png_files:
        print(file)

    # Now move them to the git repo (if not already there)
    for file in png_files:
        # Move the files to the correct location if needed
        # subprocess.run(f"cp {file} path_to_your_git_repo/your_assets_folder", shell=True)

    # Upload to GitHub
        upload_to_github()

else:
    print("No PNG files found.")
