from django.db import models
import uuid


class Product(models.Model):

    #SKU stands for ‘Stock Keeping Unit.’ It is a unique alphanumeric code that identifies 
    # a product to help retailers keep track of their inventory.
    sku = models.CharField(max_length=36, default=uuid.uuid4)
    name= models.CharField(max_length=50)
    price = models.FloatField()
    brand= models.CharField(max_length=50)
