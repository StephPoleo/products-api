from urllib import response
from django.test import SimpleTestCase
from django.test import Client
from django.urls import reverse, resolve
from ..views import UserView, ProductView
from ..serializers import UserSerializer, ProductSerializer

import json
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib import auth
from django.contrib.auth import get_user_model

User = get_user_model()

""" class TestUrls(SimpleTestCase):
    def test_products_url_is_resolved(self):
        url = reverse('product-list')
        self.assertEquals(resolve(url).func.__name__, ProductView.__name__) 

    def test_users_url_is_resolved(self):
        url = reverse('user-list')
        self.assertEquals(resolve(url).func.__name__, UserView.__name__)  """

class RegistrationTestCase(APITestCase):

    list_url = reverse('product-list')

    def test_registration(self):
        data = {"username": "testcase", "email":"testcase@test.com", "password":"test"}
        response = self.client.post("/auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_list_authenticated(self):
    
        user = User.objects.create(username='test1', email='test1@test.com')
        user.set_password('12345')
        user.save()
        client = Client()
        logged_in = client.login(email='test1@test.com', password='12345')

        if logged_in:
            response = self.client.get(self.list_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_detail_authenticated(self):
        user = User.objects.create(username='test1', email='test1@test.com')
        user.set_password('12345')
        user.save()
        client = Client()
        logged_in = client.login(email='test1@test.com', password='12345')

        data = {"name": "product", "price":1000, "brand":"product brand"}
        response = self.client.post("/products/", data)

        print(response)

        if logged_in:
            response = self.client.get(reverse("product-detail", kwargs={"pk":1}))
            print(response.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            #self.assertEqual(response.data["user"])

    def test_product_list_unauthenticated(self):
        client = self.client
        user = auth.get_user(client)
        if user.is_anonymous:
            response = self.client.get(self.list_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)