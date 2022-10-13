from dataclasses import field
from rest_framework import serializers
from .models import Product, User

class ProductSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk',
        )

    class Meta:
        model = Product
        fields = ('name', 'price', 'brand', 'url')

class UserSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='user-detail',
        lookup_field='pk',
        )

    class Meta:
        model = User
        fields = ('username', 'email', 'url')