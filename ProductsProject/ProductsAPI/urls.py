from xml.etree.ElementInclude import include
from django.urls import path, include
from . import views
from rest_framework import routers

router= routers.SimpleRouter()
router.register(r'products', views.ProductView)
router.register(r'users', views.UserView)

urlpatterns = [
    path('', include(router.urls)),
]