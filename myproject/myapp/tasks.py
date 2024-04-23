import numpy as np
from sklearn.cluster import KMeans
from PIL import Image as PilImage
from io import BytesIO
import os

from myproject.settings import BASE_DIR


async def process_image_async(image_path, n_colors, image_instance):
    image = PilImage.open(image_path)

    #Convert image to array
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


    #Store centroids
    centroids = kmeans.cluster_centers_

    #Send centroids to Centroids function in order to save to database
    save_centroids_to_model(image_instance, centroids)

    # Recreate image with quantized colors
    def recreate(centroids, labels, w, h):
        quantized_image = np.zeros((w * h, 3))
        for i in range(w * h):
            quantized_image[i] = centroids[labels[i]]
        return quantized_image.reshape((w, h, 3))

    quantized_image = recreate(kmeans.cluster_centers_, labels, w, h)

    processed_image = PilImage.fromarray((quantized_image * 255).astype(np.uint8))


    #Save image
    
    original_filename = os.path.basename(image_path)
    processed_image_name = f"{os.path.splitext(original_filename)[0]}_processed.jpg"

    processed_image_io = BytesIO()
    processed_image.save(processed_image_io, format='JPEG')
    processed_image_io.seek(0)

    processed_image_path = os.path.join(BASE_DIR, 'media', 'processed_images', processed_image_name)
    
    processed_image_content = BytesIO()
    processed_image.save(processed_image_content, format='JPEG')
    processed_image_content.seek(0)
    #Get colors that image simplified to
    original_colors = np.unique(kmeans.cluster_centers_, axis=0)

    #Make colors able to displayed on HTML page
    color_html_content = ""
    for color in original_colors:
        color_hex = '#{0:02x}{1:02x}{2:02x}'.format(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
        color_html_content += f"<div style='width: 100px; height: 100px; background-color: {color_hex};'></div>"

    # Append color HTML content to existing HTML file
    with open('list.html', 'a') as html_file:
        html_file.write(color_html_content)
    return processed_image_content, color_html_content

def save_centroids_to_model(image_instance, centroids):
    n_colors = centroids.shape[0]
    for i in range(n_colors):
        setattr(image_instance, f'color{i+1}', rgb_to_hex(centroids[i]))
    

def rgb_to_hex(rgb):
    # Convert RGB values to hexadecimal color code
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))


async def generate_palette(image_path):

    # Convert image data to numpy array
    img = PilImage.open(image_path)
    print("img size", img.size)

    imagearr = np.array(img)
    imagearr = imagearr.astype('float64')
    imagearr = imagearr / 255

    w, h, d = imagearr.shape
    assert d == 3  # Ensure the image has 3 channels (RGB)

    # Reshape array
    a = w * h
    imagearr = np.reshape(imagearr, (a, d))
        
    # Call the palette function
    palette_img = await palette(imagearr)
        
        # Return the palette image path or data in the response
    return palette_img  # Or any other response data
    

async def palette(cluster_centers):
    # Convert cluster centers to integers
    cluster_centers = cluster_centers.astype(int)

    # Create a blank palette image with dimensions based on the number of clusters
    num_colors = len(cluster_centers)
    palette_width = 100  # Width of each color block in the palette
    palette_height = 100  # Height of the palette image
    palette_img = np.zeros((palette_height, palette_width * num_colors, 3), dtype=np.uint8)

    # Fill the palette image with representative colors
    for i, color in enumerate(cluster_centers):
        start_col = i * palette_width
        end_col = (i + 1) * palette_width
        palette_img[:, start_col:end_col] = color

    return palette_img
 