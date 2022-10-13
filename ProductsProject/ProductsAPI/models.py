from email.policy import default
from enum import unique
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid

class Product(models.Model):

    #SKU stands for ‘Stock Keeping Unit.’ It is a unique alphanumeric code that identifies 
    # a product to help retailers keep track of their inventory.
    sku = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True)
    name= models.CharField(max_length=50)
    price = models.FloatField()
    brand= models.CharField(max_length=50)

    # Funcion que nos permite ver el nombre del producto directamente en Django Admin
    def __str__(self):
        return self.name

class Manager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have a email")

        if not username:
            raise ValueError("Users must have an username")

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser):

    username= models.CharField(max_length=50)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    is_Admin = models.BooleanField(default= False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['username']

    objects = Manager()

    # Funcion que nos permite ver el nombre del producto directamente en Django Admin
    def __str__(self):
        return self.username

    def has_perm(self, perm, obj= None):
        return self.is_Admin
    
    def has_module_perms(self,app_label):
        return True