from xml.etree.ElementInclude import include
from django.urls import path
from . import views
from rest_framework import routers

router= routers.DefaultRouter()
router.register('products', views.ProductView)

urlpatterns = [
    path('', include(router.urls)),
]