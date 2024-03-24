from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Image(models.Model):
    name = models.CharField(max_length=40)
    numberOfColors = models.IntegerField(default=6, validators=[MinValueValidator(2), MaxValueValidator(8)])
    image = models.ImageField(upload_to='image/', default='media/image/DJI_0030.jpg')
    simplifiedImage = models.ImageField(upload_to='simplifiedImage/')
    
    #Delete image file alone with column
    def delete(self):
        self.image.delete()
        super().delete()