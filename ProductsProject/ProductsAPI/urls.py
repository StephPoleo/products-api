from xml.etree.ElementInclude import include
from django.urls import path, include
from . import views
from rest_framework import routers

# Creating dynamic rounting for user Model
router= routers.DefaultRouter()
router.register(r'users', views.UserView, basename='user') 

urlpatterns = [
    path('', include(router.urls)),
    path('products/', views.ProductView.as_view(), name='product'),
    path('products/<uuid:sku>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('analytics/', views.AnalyticsView.as_view(), name='analytics')
]