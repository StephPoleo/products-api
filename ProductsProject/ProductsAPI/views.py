from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import mixins, viewsets, permissions
from rest_framework.views import APIView
from rest_framework import status
from .models import Product, User
from .serializers import ProductSerializer, UserSerializer

# View for User custom model
class UserView(viewsets.ModelViewSet):
    queryset= User.objects.all()
    serializer_class = UserSerializer
    # The only way to create, see or edit users is for authenticated users
    permission_classes = [permissions.IsAuthenticated]

# View for Product model
class ProductView(viewsets.ModelViewSet):
    queryset= Product.objects.all()
    serializer_class = ProductSerializer
    # Anonymous users can see products, but not create or edit them
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]