from django.test import TestCase

# Create your tests here.

import os

# Path to the directory where uploaded files are stored
upload_dir = 'Q:\Bellarmine\VisualStudio\Capstone\myproject\media\processed_images'

# Check if the directory exists
if os.path.isdir(upload_dir):
    # Check read permission for the directory
    if os.access(upload_dir, os.R_OK):
        print(f"Django server has read permission for the directory: {upload_dir}")
    else:
        print(f"Django server does not have read permission for the directory: {upload_dir}")
else:
    print(f"Directory does not exist: {upload_dir}")