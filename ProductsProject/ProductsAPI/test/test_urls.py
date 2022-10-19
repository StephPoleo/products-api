from django.test import Client
from django.urls import reverse
from ..models import User, Product

import json
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib import auth
from django.contrib.auth import get_user_model

from django.core import mail

User = get_user_model()

class RegistrationTestCase(APITestCase):

    product_list_url = reverse('product-list')
    user_list_url = reverse('user-list')

    # Testing login
    def test_registration(self):
        data = {"username": "testcase", "email":"testcase@test.com", "password":"test"}
        response = self.client.post("/auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing GET ALL users when authenticated
    def test_users_list_authenticated(self):
    
        user = User.objects.create(username='test1', email='test1@test.com')
        user.set_password('12345')
        user.save()
        client = Client()
        logged_in = client.login(email='test1@test.com', password='12345')

        if logged_in:
            response = client.get(self.user_list_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing GET ALL users when user is anonymous
    def test_users_list_unauthenticated(self):

        client = self.client
        user = auth.get_user(client)
        if user.is_anonymous:
            response = client.get(self.user_list_url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(json.loads(response.content)['detail'], "Authentication credentials were not provided.")

    # Testing GET by id users when authenticathed
    def test_user_detail_authenticated(self):
        user = User.objects.create(username='test1', email='test1@test.com')
        user.set_password('12345')
        user.save()
        client = Client()
        logged_in = client.login(email='test1@test.com', password='12345')

        if logged_in:
            response = client.get(reverse("user-detail", kwargs={"pk":user.id}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing GET by id users when user is anonymous
    def test_user_detail_unauthenticated(self):
        client = self.client
        user = auth.get_user(client)

        if user.is_anonymous:
            response = client.get(reverse("user-detail", kwargs={"pk":user.id}))
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(json.loads(response.content)['detail'], "Authentication credentials were not provided.")

    # Testing POST user when authenticathed
    def test_post_user_detail_authenticated(self):
        user = User.objects.create(username='test1', email='test1@test.com')
        user.set_password('12345')
        user.save()
        client = Client()
        logged_in = client.login(email='test1@test.com', password='12345')

        data = {"username": "testcase", "email":"testcase@test.com", "password":"test"}

        if logged_in:
            response =  client.post(self.user_list_url, data=data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Testing POST user when user is anonymous
    def test_post_user_detail_unauthenticated(self):
        client = self.client
        user = auth.get_user(client)
        data = {"username": "testcase", "email":"testcase@test.com", "password":"test"}

        if user.is_anonymous:
            response =  client.post(self.user_list_url, data=data)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Testing PUT user by id when authenticathed
    def test_modify_user_detail_authenticated(self):
        user = User.objects.create(username='test1', email='test1@test.com')
        user.set_password('12345')
        user.save()
        client = Client()
        logged_in = client.login(email='test1@test.com', password='12345')

        if logged_in:
            url = reverse("user-detail", kwargs={"pk":user.id})
            data = {"username": "test1", "email":"test1@test.com", "password":"test"}
            response = client.put(url, data=data, content_type='application/json')
            user.refresh_from_db()
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing PUT user by id when user is anonymous
    def test_modify_user_detail_unauthenticated(self):
        client = self.client
        user = auth.get_user(client)

        if user.is_anonymous:
            url = reverse("user-detail", kwargs={"pk":user.id})
            data = {"username": "test1", "email":"test1@test.com", "password":"test"}
            response = client.put(url, data=data, content_type='application/json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Testing DELETE user by id when authenticathed
    def test_delete_user_detail_authenticated(self):
        user = User.objects.create(username='test1', email='test1@test.com')
        user.set_password('12345')
        user.save()
        client = Client()
        logged_in = client.login(email='test1@test.com', password='12345')

        if logged_in:
            url = reverse("user-detail", kwargs={"pk":user.id})
            response = client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) 

    # Testing DELETE user by id when user is anonymous
    def test_delete_user_detail_unauthenticated(self):
        client = self.client
        user = auth.get_user(client)

        if user.is_anonymous:
            url = reverse("user-detail", kwargs={"pk":user.id})
            response = client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Testing GET ALL products when authenticathed
    def test_product_list_authenticated(self):
    
        user = User.objects.create(username='test1', email='test1@test.com')
        user.set_password('12345')
        user.save()
        client = Client()
        logged_in = client.login(email='test1@test.com', password='12345')

        Product.objects.create(name = "product name", price = 1000, brand = "product brand")

        if logged_in:
            response = client.get(self.product_list_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing GET ALL products when user is anonymous
    def test_product_list_unauthenticated(self):
        Product.objects.create(name = "product name", price = 1000, brand = "product brand")

        client = self.client
        user = auth.get_user(client)
        if user.is_anonymous:
            response = client.get(self.product_list_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing GET by sku products when authenticathed
    def test_product_detail_authenticated(self):
        user = User.objects.create(username='test1', email='test1@test.com')
        user.set_password('12345')
        user.save()
        client = Client()
        logged_in = client.login(email='test1@test.com', password='12345')

        product = Product.objects.create(name = "product name", price = 1000, brand = "product brand")

        if logged_in:
            response = client.get(reverse("product-detail", kwargs={"pk":product.sku}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing GET by sku products when user is anonymous
    def test_product_detail_unauthenticated(self):
        client = self.client
        user = auth.get_user(client)
        product = Product.objects.create(name = "product name", price = 1000, brand = "product brand")

        if user.is_anonymous:
            response = client.get(reverse("product-detail", kwargs={"pk":product.sku}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing POST product when authenticathed
    def test_post_product_detail_authenticated(self):
        user = User.objects.create(username='test1', email='test1@test.com')
        user.set_password('12345')
        user.save()
        client = Client()
        logged_in = client.login(email='test1@test.com', password='12345')

        data = {"name": "product name", "price":100, "brand":"product brand"}

        if logged_in:
            response =  client.post(self.product_list_url, data=data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Testing POST product when user is anonymous
    def test_post_product_detail_unauthenticated(self):
        client = self.client
        user = auth.get_user(client)
        data = {"name": "product name", "price":100, "brand":"product brand"}

        if user.is_anonymous:
            response =  client.post(self.product_list_url, data=data)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Testing PUT by sku products when authenticathed
    def test_modify_product_detail_authenticated(self):
        user = User.objects.create(username='test1', email='test1@test.com')
        user.set_password('12345')
        user.save()
        client = Client()
        logged_in = client.login(email='test1@test.com', password='12345')

        product = Product.objects.create(name = "product name", price = 1000, brand = "product brand")

        if logged_in:
            url = reverse("product-detail", kwargs={"pk":product.sku})
            data = {"name": "product", "price":2000, "brand":"product brand"}
            response = client.put(url, data=data, content_type='application/json')
            product.refresh_from_db()
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            User.objects.create(username='test2', email='test2@test.com')
            response = client.get(self.user_list_url)

            subject = 'subject'
            body = 'body'
            from_email = 'from_email@test.com'
            recipient_list = []

            for value in json.loads(response.content):
                recipient_list.append(value.get('email'))
            
            messages = [(subject, body, from_email, [r]) for r in recipient_list]

            mail.outbox = []
            mail.send_mass_mail(messages) 
            self.assertEqual(len(mail.outbox), 2)

    # Testing PUT by sku products when user is anonymous
    def test_modify_product_detail_unauthenticated(self):
        client = self.client
        user = auth.get_user(client)
        product = Product.objects.create(name = "product name", price = 1000, brand = "product brand")

        if user.is_anonymous:
            url = reverse("product-detail", kwargs={"pk":product.sku})
            data = {"name": "product", "price":2000, "brand":"product brand"}
            response = client.put(url, data=data, content_type='application/json')
            product.refresh_from_db()
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Testing DELETE by sku products when authenticathed
    def test_delete_product_detail_authenticated(self):
        user = User.objects.create(username='test1', email='test1@test.com')
        user.set_password('12345')
        user.save()
        client = Client()
        logged_in = client.login(email='test1@test.com', password='12345')

        product = Product.objects.create(name = "product name", price = 1000, brand = "product brand")

        if logged_in:
            url = reverse("product-detail", kwargs={"pk":product.sku})
            response = client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Testing DELETE by sku products when user is anonymous
    def test_delete_product_detail_unauthenticated(self):
        client = self.client
        user = auth.get_user(client)
        product = Product.objects.create(name = "product name", price = 1000, brand = "product brand")

        if user.is_anonymous:
            url = reverse("product-detail", kwargs={"pk":product.sku})
            response = client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

