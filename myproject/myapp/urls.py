from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.list_images, name="list_images"),
    path("home/", views.home, name="home"),
    path("delete/<int:pk>/", views.delete_image, name='delete_image')
]