from django.urls import path
from . import views
from myapp import consumers
from django.conf.urls import include
from myapp.routing import websocket_urlpatterns

urlpatterns = [
    path("list/", views.list_images, name="list_images"),
    path("home/", views.home, name="home"),
    path("delete/<int:pk>/", views.delete_image, name='delete_image'),
]

urlpatterns += websocket_urlpatterns
