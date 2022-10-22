from cmath import exp
from datetime import datetime
from unittest import result
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import mixins, viewsets, permissions, generics
from rest_framework.viewsets import ViewSetMixin
from rest_framework.views import APIView
from rest_framework import status
from .models import Product, User
from .serializers import ProductSerializer, UserSerializer
from django.urls import reverse
from django.shortcuts import redirect

import pandas as pd
import os
import csv 
import json 

# View for User custom model
class UserView(viewsets.ModelViewSet):
    queryset= User.objects.all()
    serializer_class = UserSerializer
    # The only way to create, see or edit users is for authenticated users
    permission_classes = [permissions.IsAuthenticated]

# View for Product model, for GET and POST methods
class ProductView(generics.ListCreateAPIView):

    queryset= Product.objects.all()
    serializer_class = ProductSerializer
    # Anonymous users can see products, but not create or edit them
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # GET all products
    def list(self, request):
        
        # Checking if there is a previous log file
        try:
            df = pd.read_csv('analytics/users_requests.csv')
        
        # If not, create a new one
        except Exception:
            df = pd.DataFrame()

        # In case there is not a session, we create one to detect the users 
        # requesting information from the API
        if not request.session or not request.session.session_key:
            request.session.save()

        # Detecting and saving anonymous user information
        if(not request.session.items()):
            user_id = request.session.session_key
            user_name = 'Anonymous'

        # Detecting and saving logged user information
        else:
            user_id = int(request.session['_auth_user_id'])
            user_name = User.objects.get(id=request.session['_auth_user_id'])

        # Saving the extracted information into a Dataframe, to perform further analysis
        new = {'User ID': user_id,
                'User name': str(user_name),
                'Method': str(request.method),
                'Time': datetime.now(),
                'Product': 'All', 
                'SKU': '-'}

        df = df.append(new, ignore_index=True)

        # Creating the directory if it does not exist, and converting the dataframe
        # into a CSV file.
        os.makedirs('analytics', exist_ok=True)  
        df.to_csv('analytics/users_requests.csv', index = False)

        # Getting the stored information and sending it to the API
        queryset = self.get_queryset()
        serializer_context = {
            'request': request,
        }
        serializer = ProductSerializer(queryset, context=serializer_context, many=True) 
        return Response(serializer.data)

    # Create a product a save it into the database
    def post(self, request):

        # Checking if there is a previous log file
        try:
            df = pd.read_csv('analytics/users_requests.csv')
        
        # If not, create a new one
        except Exception:
            df = pd.DataFrame()
        
        # Getting the user information 
        user_name = User.objects.get(id=request.session['_auth_user_id'])
        serializer = ProductSerializer(data = request.data)

        # Saving the extracted information into a Dataframe, to perform further analysis
        if serializer.is_valid():
            serializer.save()
            new = {'User ID': request.session['_auth_user_id'],
                'User name': str(user_name), 
                'Method': str(request.method),
                'Time': datetime.now(),
                'Product':serializer.data['name'], 
                'SKU': serializer.data['sku']}

            df = df.append(new, ignore_index=True)

            os.makedirs('analytics', exist_ok=True)  
            df.to_csv('analytics/users_requests.csv', index = False)

            return Response(serializer.data)
        else:
            return Response(serializer.errors)

# View for Product details, using GET, PUT and DELETE
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ProductSerializer
    # Anonymous users can see products, but not create or edit them
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Get method by sku
    def retrieve(self, request, *args, **kwargs):

        # Checking if there is a previous log file
        try:
            df = pd.read_csv('analytics/users_requests.csv')
        
        # If not, create a new one
        except Exception:
            df = pd.DataFrame()

        # In case there is not a session, we create one to detect the users 
        # requesting information from the API
        if not request.session or not request.session.session_key:
            request.session.save()

        # Detecting and saving anonymous user information
        if(not request.session.items()):
            user_id = request.session.session_key
            user_name = 'Anonymous'

        # Detecting and saving logged user information
        else:
            user_id = int(request.session['_auth_user_id'])
            user_name = User.objects.get(id=request.session['_auth_user_id'])

        # Getting the product information
        object = Product.objects.get(pk=kwargs['sku'])
        serializer = ProductSerializer(object)

        # Saving the extracted information into a Dataframe, to perform further analysis
        new = {'User ID': user_id,
                'User name': str(user_name),
                'Method': str(request.method),
                'Time': datetime.now(),
                'Product':serializer.data['name'], 
                'SKU': serializer.data['sku']}

        df = df.append(new, ignore_index=True)

        # Creating the directory if it does not exist, and converting the dataframe
        # into a CSV file.
        os.makedirs('analytics', exist_ok=True)  
        df.to_csv('analytics/users_requests.csv', index = False)

        return Response(serializer.data)

    # PUT method
    def put(self, request, *args, **kwargs):
        # Checking if there is a previous log file
        try:
            df = pd.read_csv('analytics/users_requests.csv')
        
        # If not, create a new one
        except Exception:
            df = pd.DataFrame()

        # Getting the user information
        user_name = User.objects.get(id=request.session['_auth_user_id'])

        # Getting the product information
        sku = self.kwargs.get('sku')
        product = Product.objects.filter(sku = sku).first()
        serializer = ProductSerializer(product, data = request.data, partial=True)

        # Saving the extracted information into a Dataframe, to perform further analysis
        if serializer.is_valid():
            serializer.save()
            new = {'User ID': request.session['_auth_user_id'],
                'User name': str(user_name),
                'Method': str(request.method),
                'Time': datetime.now(),
                'Product':serializer.data['name'], 
                'SKU': serializer.data['sku']}

            df = df.append(new, ignore_index=True)

            # Creating the directory if it does not exist, and converting the dataframe
            # into a CSV file.
            os.makedirs('analytics', exist_ok=True)  
            df.to_csv('analytics/users_requests.csv', index = False)

            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    # DELETE method
    def delete(self, request, *args, **kwargs):
        # Checking if there is a previous log file
        try:
            df = pd.read_csv('analytics/users_requests.csv')
        
        # If not, create a new one
        except Exception:
            df = pd.DataFrame()

        # Getting the user information
        user_name = User.objects.get(id=request.session['_auth_user_id'])

        # Getting the product information
        sku = self.kwargs.get('sku')
        product = Product.objects.filter(sku = sku).first()
        serializer = ProductSerializer(product, data = request.data, partial=True)

        # Saving the extracted information into a Dataframe, to perform further analysis
        if serializer.is_valid():
            new = {'User ID': request.session['_auth_user_id'], 
                'User name': str(user_name),
                'Method': str(request.method),
                'Time': datetime.now(),
                'Product':serializer.data['name'], 
                'SKU': serializer.data['sku']}

            df = df.append(new, ignore_index=True)

            # Creating the directory if it does not exist, and converting the dataframe
            # into a CSV file.
            os.makedirs('analytics', exist_ok=True)  
            df.to_csv('analytics/users_requests.csv', index = False)

            # After all the needed information is stored, delete the product
            product.delete()
            return redirect('/products/')
        else:
            return Response(serializer.errors)

# View for showing the analytics
class AnalyticsView(APIView):

    # Get method for analytics
    def get(self, request):
        # Open the file
        try:
            df = pd.read_csv('analytics/users_requests.csv')

        # If it does not exist, create a blank dataframe  
        except Exception:
            df = pd.DataFrame()

        # Get the statistic summary from the information
        df = df.describe()

        # Turn it into a JSON
        result = df.to_json(orient="split")
        parsed = json.loads(result)

        # If the information says 'All', it means that the request was to
        # the main page with the list of all the products
        if(parsed['data'][2][4] == 'All'):
            most_frequent_product = 'General browsing on main list'

        # Get the most frequent product 
        else:
            most_frequent_product = parsed['data'][2][4]

        # Get the most frequent hour for the requests
        most_frequent_hour = str(parsed['data'][2][3]).split(' ')[1]
        most_frequent_hour = most_frequent_hour.split('.')[0]
        most_frequent_hour = most_frequent_hour.split(':')
        most_frequent_hour = most_frequent_hour[0] + ':' + most_frequent_hour[1]

        # Create a final JSON with all the information
        final_json = {
            "amount of APIs requests": parsed['data'][0][0],
            "different user IDs": parsed['data'][1][0],
            "different products requested" : parsed['data'][1][4],
            "top user": parsed['data'][2][1],
            "most frequent method": parsed['data'][2][2],
            "most requested product": most_frequent_product,
            "top requesting hour": most_frequent_hour
        }

        return Response(final_json)
