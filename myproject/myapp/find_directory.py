import os

# Get the base directory of your Django project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define the relative path to the directory containing your images
images_directory = os.path.join(BASE_DIR, 'data')

# Print the absolute path to the images directory
print("Absolute path to images directory:", images_directory)