import asyncio
import math
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image as PilImage
from django.core.files.base import ContentFile
from io import BytesIO
import io
import os


async def process_image_async(image_path, n_colors):
    image = PilImage.open(image_path)
    wimage = math.floor(image.width/2)
    himage = math.floor(image.height/2)
    image = image.resize((wimage, himage))

    imagearr = np.array(image)
    imagearr = imagearr.astype('float64')
    imagearr = imagearr / 255

    w, h, d = imagearr.shape
    assert d == 3  # Ensure the image has 3 channels (RGB)

    # Reshape array
    a = w * h
    imagearr = np.reshape(imagearr, (a, d))

    # Fit K-Means model
    kmeans = KMeans(n_clusters=n_colors, random_state=0)
    kmeans.fit(imagearr)

    # Get labels
    labels = kmeans.predict(imagearr)

    # Print labels for debugging
    print("Labels:", labels)

    # Print centroids for debugging
    print("Centroids of quantized colors:", kmeans.cluster_centers_)


    # Recreate image with quantized colors
    def recreate(centroids, labels, w, h):
        quantized_image = np.zeros((w * h, 3))
        for i in range(w * h):
            quantized_image[i] = centroids[labels[i]]
        return quantized_image.reshape((w, h, 3))

    quantized_image = recreate(kmeans.cluster_centers_, labels, w, h)

    processed_image = PilImage.fromarray((quantized_image * 255).astype(np.uint8))

    original_filename = os.path.basename(image_path)
    processed_image_name = f"{os.path.splitext(original_filename)[0]}_processed.jpg"

    processed_image_io = BytesIO()
    processed_image.save(processed_image_io, format='JPEG')
    processed_image_io.seek(0)

    processed_image_file = ContentFile(processed_image_io.read(), name=processed_image_name)

    return processed_image_file