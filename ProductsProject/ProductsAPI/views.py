from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from .models import Product, User
from .serializers import ProductSerializer, UserSerializer

class ProductView(viewsets.ModelViewSet):
    queryset= Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class UserView(viewsets.ModelViewSet):
    queryset= User.objects.all()
    serializer_class = UserSerializer

