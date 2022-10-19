from dataclasses import field
from rest_framework import serializers
from .models import Product, User

class ProductSerializer(serializers.HyperlinkedModelSerializer):

    # Stablishing a url to take the user to the product detail page, so modifying the endpoit to see specific information will not be necessary
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk',
        )

    class Meta:
        model = Product
        fields = ('name', 'price', 'brand', 'url')

class UserSerializer(serializers.HyperlinkedModelSerializer):

    # Stablishing a url to take the user to the user detail page, so modifying the endpoit to see specific information will not be necessary
    url = serializers.HyperlinkedIdentityField(
        view_name='user-detail',
        lookup_field='pk',
        )

    # Password field will be write only, when creating and editing an user
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'url')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    # Creating funtions for creating and updating the password for the custom User
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance = super(UserSerializer, self).update(instance, validated_data)
        instance.set_password(validated_data['password'])
        instance.is_active = True
        instance.save()
        return instance