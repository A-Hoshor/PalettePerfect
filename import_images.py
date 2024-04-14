import os
import sys
import django

# Add the path to your Django project directory to sys.path
sys.path.append(r"Q:\Bellarmine\VisualStudio\Capstone\myproject")

# Set the DJANGO_SETTINGS_MODULE environment variable to your project's settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Initialize Django
django.setup()

from django.core.files import File
from myapp.models import BookCovers

def import_images_from_directory(main_directory):
    for subject_folder in os.listdir(main_directory):
        subject_path = os.path.join(main_directory, subject_folder)
        if os.path.isdir(subject_path):
            import_images_from_subject(subject_path)

def import_images_from_subject(subject_directory):
    print("Importing images from subject:", os.path.basename(subject_directory))
    for filename in os.listdir(subject_directory):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(subject_directory, filename)
            with open(image_path, 'rb') as f:
                book_cover = BookCovers()
                book_cover.bookImage.save(filename, File(f))
                book_cover.save()
    print("Import process for subject completed.")

if __name__ == "__main__":
    # Define the main directory path where subject folders are located
    main_directory = r"Q:\Bellarmine\VisualStudio\Capstone\data\book-covers"

    # Import images from each subject folder
    import_images_from_directory(main_directory)