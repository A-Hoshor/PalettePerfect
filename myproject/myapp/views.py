import asyncio
from django.shortcuts import render, get_object_or_404, redirect
from myapp.forms import ImageForm
from myapp.models import Image
from .tasks import process_image_async
from asgiref.sync import sync_to_async
from django.core.files.base import ContentFile



# Create your views here.
async def async_process_image(image_instance, number_of_colors):
    # save the processed image to the database
    # Call the async function to process the image
    processed_image = await process_image_async(image_instance.image.path, number_of_colors)

    # Save the processed image to the database
    image_instance.processed_image.save(processed_image.name, processed_image, save=False)

    await sync_to_async(image_instance.save)()


async def home(request):
    if request.method =="POST":
        print("form data:", request.POST)
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            print("form is valid!")
            image_instance = form.save(commit=False)
            numberOfColors = form.cleaned_data["numberOfColors"]
            name = form.cleaned_data["name"]
            image_instance.numberOfColors = numberOfColors
            image_instance.name = name

            # Save the original uploaded image
            await sync_to_async(image_instance.save)()

            # Apply color quantization algorithm
            await async_process_image(image_instance, numberOfColors)

            return redirect('list_images')
        else:
            print("form is not valid!")
            context = {'form': form}
            return render(request, "home.html", context)
    context = {'form': ImageForm()}
    return render(request, "home.html", context)

async def list_images(request):
    images = await sync_to_async(list)(Image.objects.all())
    context = {'images': images}
    return render(request, 'list.html', context)

async def delete_image(request, pk):
    image = await sync_to_async(get_object_or_404)(Image, pk=pk)
    await sync_to_async(image.delete)()
    return redirect('list_images')

