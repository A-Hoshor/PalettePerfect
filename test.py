import matplotlib.pyplot as plt
import numpy as np
from numpy import asarray
from sklearn.cluster import KMeans
from PIL import Image
from sklearn.metrics import pairwise_distances_argmin
from sklearn.utils import resample

n_colors = 8

image_path=("img/drone.JPG")
image=Image.open(image_path)

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
labels_random = pairwise_distances_argmin(book, imagearr, axis=0)

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