import asyncio
import base64
import random
from django.shortcuts import render, get_object_or_404, redirect
from myapp.forms import ImageForm
from myapp.models import Image
from myproject.settings import BASE_DIR
from .tasks import process_image_async, generate_palette
from asgiref.sync import sync_to_async
from django.core.files.base import ContentFile
import os
import logging
from django.shortcuts import redirect
from django.conf import settings
from django.core.files.storage import default_storage
from concurrent.futures import ThreadPoolExecutor
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import Http404

# Create your views here.
async def async_process_image(image_instance, number_of_colors, original_name, processed_image_content):
  

    # Save the processed image to the database
    processed_image_name = f"{os.path.splitext(original_name)[0]}_processed.jpg"
    image_instance.processed_image.save(processed_image_name, processed_image_content, save=False)
    await sync_to_async(image_instance.save)()

async def home(request):
    if request.method =="POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                print("Form is valid")
                image_instance = form.save(commit=False)
                numberOfColors = form.cleaned_data["numberOfColors"]
                name = form.cleaned_data["name"]
                image_instance.numberOfColors = numberOfColors
                image_instance.name = name
                original_name = request.FILES['image'].name

                # Save the image instance
                print('saving image instance to database....')
                await sync_to_async(image_instance.save)()

                print("Uploaded file:", request.FILES['image'])

                #construct path
                image_path = os.path.join(BASE_DIR, 'media', 'image', original_name)
                image_instance.image = image_path
                print("Image path set from request:", image_instance.image)

                print("Original image name:", original_name)
                print("Image exists:", os.path.exists(image_instance.image.path))

                # Process the image asynchronously
                print("processing image....")
                processed_image_content, color_html_content = await process_image_async(image_instance.image.path, numberOfColors, image_instance)
                print("processing image done")
                processed_image_name = f"{os.path.splitext(original_name)[0]}_processed.jpg"
                print("processed image name: ", processed_image_name)

            
               # Save the processed image to the database and get the processed image object
                processed_image_instance = await async_process_image(image_instance, numberOfColors, original_name, processed_image_content)

                print("Processed image instance", processed_image_instance)
                print("Processed image content: ", processed_image_content)
                #print("Color HTML content: ", color_html_content)

                # Pass processed image file and color HTML content to template
                context = {
                    'form': ImageForm(),
                    'processed_image': processed_image_content,
                    'color_html_content': color_html_content
                }
                #print("Context: ", context)
            
                return await list_images(request)
            except Exception as e:
                # Return an error response if an exception occurs
                return render(request, "error.html", {"error_message": "An error occurred while processing the image."})
        else:
            # Return the form with errors if it's not valid
            context = {'form': form}
            return render(request, "home.html", context)
    else:
        print("Returning home.html template for GET request")
        context = {'form': ImageForm()}
        return render(request, "home.html", context)

async def list_images(request):
    try:
        images = await sync_to_async(list)(Image.objects.all())
    except Exception as e:
        print("An error occurred while fetching images:", e)
        images = []

    context = {
        'images': images,
    }

    #print("Context in list_images:", context)  # Check the context before rendering the template

    return render(request, 'list.html', context)

def color_list(request):
    colors = Image.colors.all()
    return render(request, 'your_template.html', {'colors': colors})

async def delete_image(request, pk):
    image = await sync_to_async(get_object_or_404)(Image, pk=pk)
    await sync_to_async(image.delete)()
    return redirect('list_images')

def color_info(request, pk):
    # Handle GET request to render the template
    image = Image.objects.get(pk=pk)
    
    # Pass the processed image to the template
    context = {
        'pk': pk,
        'processed_image': image.processed_image.url,  
        'colors': [image.color1, image.color2, image.color3, image.color4, image.color5, image.color6, image.color7, image.color8]
    }

    print(context)
    
    return render(request, 'color_info.html', context)


def generate_random_color():
    """Generate a random color represented as RGB tuple."""
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

def generate_random_colors(num_colors):
    """Generate a list of random colors."""
    return [generate_random_color() for _ in range(num_colors)]

# Generate 4 to 6 random colors
num_colors = random.randint(4, 6)
random_colors = generate_random_colors(num_colors)

print("Random colors:", random_colors)

def randomize_image(request, pk):
    print("Inside randomize_image view function")
    print("Primary key(pk): ", pk)

    if request.method == 'POST':
        num_colors = 8
        random_colors = generate_random_colors(num_colors)
        print(random_colors)

        # Fetch the processed image URL based on the primary key (pk)
        try:
            image = Image.objects.get(pk=pk)
            processed_image_url = image.processed_image.url
            print("Processed image URL:", processed_image_url)
        except Image.DoesNotExist:
            processed_image_url = None

        # Include the pk parameter in the context
        context = {
            'random_colors': random_colors,
            'processed_image_url': processed_image_url,
            'pk': pk,  # Add pk to the context
        }
        return render(request, 'random.html', context)
    else:
        # Your existing code to render the initial template
        return render(request, 'color_info.html')