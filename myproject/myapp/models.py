from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Image(models.Model):
    name = models.CharField(max_length=40)
    numberOfColors = models.IntegerField(default=6, validators=[MinValueValidator(2), MaxValueValidator(8)])
    image = models.ImageField(upload_to='image/')
    processed_image = models.ImageField(upload_to='processed_images/', blank=True, null=True)
    color1 = models.CharField(max_length=7, blank=True, null=True)  # Assuming storing hex code like '#FFFFFF'
    color2 = models.CharField(max_length=7, blank=True, null=True)
    color3 = models.CharField(max_length=7, blank=True, null=True)
    color4 = models.CharField(max_length=7, blank=True, null=True)
    color5 = models.CharField(max_length=7, blank=True, null=True)
    color6 = models.CharField(max_length=7, blank=True, null=True)
    color7 = models.CharField(max_length=7, blank=True, null=True)
    color8 = models.CharField(max_length=7, blank=True, null=True)

    
    #Delete image file alone with column
    def delete(self):
        self.image.delete()
        super().delete()

    #Read image
    def read_image(self):
        with open(self.image.path, 'rb') as f:
            return f.read()
        
    #Read color values
    def __str__(self):
        return self.name
