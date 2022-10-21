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

# View for Product model
class ProductView(generics.ListCreateAPIView):

    queryset= Product.objects.all()
    serializer_class = ProductSerializer
    # Anonymous users can see products, but not create or edit them
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request):
        
        try:
            df = pd.read_csv('analytics/users_requests.csv')
        
        except Exception:
            df = pd.DataFrame()

        if not request.session or not request.session.session_key:
            request.session.save()

        if(not request.session.items()):
            user_id = request.session.session_key
            user_name = 'Anonymous'

        else:
            user_id = int(request.session['_auth_user_id'])
            user_name = User.objects.get(id=request.session['_auth_user_id'])

        new = {'User ID': user_id,
                'User name': str(user_name),
                'Method': str(request.method),
                'Time': datetime.now(),
                'Product': 'All', 
                'SKU': '-'}

        df = df.append(new, ignore_index=True)

        os.makedirs('analytics', exist_ok=True)  
        df.to_csv('analytics/users_requests.csv', index = False)

        queryset = self.get_queryset()
        serializer_context = {
            'request': request,
        }
        serializer = ProductSerializer(queryset, context=serializer_context, many=True) 
        return Response(serializer.data)

    def post(self, request):

        try:
            df = pd.read_csv('analytics/users_requests.csv')
        
        except Exception:
            df = pd.DataFrame()

        user_name = User.objects.get(id=request.session['_auth_user_id'])

        serializer = ProductSerializer(data = request.data)

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

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ProductSerializer
    # Anonymous users can see products, but not create or edit them
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        try:
            df = pd.read_csv('analytics/users_requests.csv')
        
        except Exception:
            df = pd.DataFrame()

        if(not request.session.items()):
            user_id = request.session.session_key
            user_name = 'Anonymous'

        else:
            user_id = int(request.session['_auth_user_id'])
            user_name = User.objects.get(id=request.session['_auth_user_id'])


        object = Product.objects.get(pk=kwargs['sku'])
        serializer = ProductSerializer(object)

        new = {'User ID': user_id,
                'User name': str(user_name),
                'Method': str(request.method),
                'Time': datetime.now(),
                'Product':serializer.data['name'], 
                'SKU': serializer.data['sku']}

        df = df.append(new, ignore_index=True)

        os.makedirs('analytics', exist_ok=True)  
        df.to_csv('analytics/users_requests.csv', index = False)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        try:
            df = pd.read_csv('analytics/users_requests.csv')
        
        except Exception:
            df = pd.DataFrame()

        user_name = User.objects.get(id=request.session['_auth_user_id'])

        sku = self.kwargs.get('sku')
        product = Product.objects.filter(sku = sku).first()
        serializer = ProductSerializer(product, data = request.data, partial=True)

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

    def delete(self, request, *args, **kwargs):
        try:
            df = pd.read_csv('analytics/users_requests.csv')
        
        except Exception:
            df = pd.DataFrame()

        user_name = User.objects.get(id=request.session['_auth_user_id'])

        sku = self.kwargs.get('sku')
        product = Product.objects.filter(sku = sku).first()
        serializer = ProductSerializer(product, data = request.data, partial=True)

        if serializer.is_valid():
            new = {'User ID': request.session['_auth_user_id'], 
                'User name': str(user_name),
                'Method': str(request.method),
                'Time': datetime.now(),
                'Product':serializer.data['name'], 
                'SKU': serializer.data['sku']}

            df = df.append(new, ignore_index=True)

            os.makedirs('analytics', exist_ok=True)  
            df.to_csv('analytics/users_requests.csv', index = False)

            product.delete()
            return redirect('/products/')
        else:
            return Response(serializer.errors)

class AnalyticsView(APIView):

    def get(self, request):
        try:
            df = pd.read_csv('analytics/users_requests.csv')
            
        except Exception:
            df = pd.DataFrame()

        df = df.describe()

        result = df.to_json(orient="split")
        parsed = json.loads(result)

        if(parsed['data'][2][4] == 'All'):
            most_frequent_product = 'General browsing on main list'
            
        else:
            most_frequent_product = parsed['data'][2][4]

        most_frequent_hour = str(parsed['data'][2][3]).split(' ')[1]
        most_frequent_hour = most_frequent_hour.split('.')[0]
        most_frequent_hour = most_frequent_hour.split(':')
        most_frequent_hour = most_frequent_hour[0] + ':' + most_frequent_hour[1]

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
