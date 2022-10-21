from xml.etree.ElementInclude import include
from django.urls import path, include
from . import views
from rest_framework import routers

# Creating dynamic rounting
router= routers.SimpleRouter()
router.register(r'products', views.ProductView, basename='product')
router.register(r'users', views.UserView, basename='user') 

urlpatterns = [
    path('', include(router.urls)),
]