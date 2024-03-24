from django.shortcuts import render, get_object_or_404, redirect
from myapp.forms import ImageForm
from myapp.models import Image


# Create your views here.

def home(request):
    if request.method =="POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            numberOfColors = ImageForm.get("numberOfColors")
            image = ImageForm.get("image")
        else:
            context = {'form': form}
            return render(request, "home.html", context)
    context = {'form': ImageForm()}
    return render(request, "home.html", context)

def list_images(request):
    images = Image.objects.all()
    context = {'images': images}
    return render(request, 'list.html', context)

def delete_image(request, pk):
    image = get_object_or_404(Image, pk=pk)
    image.delete()
    return redirect('list_images')


"""
def simplify_image():
    n_colors = 4

    image_path=("img/drone.JPG")
    image=Image.open(image_path)
    wimage = math.floor(image.width/2)
    himage = math.floor(image.height/2)
    image=image.resize((wimage, himage))

    imagearr= np.array(image)
    imagearr = imagearr.astype('float64')
    imagearr= imagearr/255

    print(imagearr)
    print(imagearr.shape)

    w=imagearr.shape[0]
    h=imagearr.shape[1]
    d=imagearr.shape[2]
    assert d == 3 #returns assertion error if not 3
    print(imagearr.shape)


    #reshape array
    a = w*h
    print(a)
    imagearr=np.reshape(imagearr,(a,d))

    #fit model on sample data
    sample=resample(imagearr,random_state=0,n_samples=1000)
    kmeans = KMeans(n_clusters=n_colors, random_state=0)
    kmeans.fit(imagearr)

    #get labels
    labels=kmeans.predict(imagearr)

    book=resample(imagearr, random_state=0, n_samples=n_colors)
    #labels_random = pairwise_distances_argmin(book, imagearr, axis=0)

    def recreate(book, labels, w, h):
        return book[labels].reshape(w,h,-1)

    print(image)

    plt.figure(1)
    plt.clf()
    plt.axis("off")
    plt.title("Original image (96,615 colors)")
    plt.imshow(image)


    plt.figure(2)
    plt.clf()
    plt.axis("off")
    plt.title(f"Quantized image ({n_colors} colors, K-Means)")
    plt.imshow(recreate(kmeans.cluster_centers_, labels, w, h))


    plt.figure(3)
    plt.clf()
    plt.axis("off")
    plt.title(f"Quantized image ({n_colors} colors, Random)")
    plt.imshow(recreate(book, labels_random, w, h))
    plt.show()
"""