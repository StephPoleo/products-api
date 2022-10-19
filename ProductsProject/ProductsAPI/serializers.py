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
        fields = ('username', 'email', 'password', 'url')
        extra_kwargs = {
            'password': {'write_only': True},
        }

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