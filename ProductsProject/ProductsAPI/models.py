from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.core.mail import send_mass_mail
import uuid

class Product(models.Model):

    #SKU stands for ‘Stock Keeping Unit.’ It is a unique alphanumeric code that identifies 
    # a product to help retailers keep track of their inventory.
    sku = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True)
    name= models.CharField(max_length=50)
    price = models.FloatField()
    brand= models.CharField(max_length=50)

    # Function that shows the model name on Django Admin
    def __str__(self):
        return self.name

# Function that manages the creation for a super user or a regular user
class Manager(BaseUserManager):
    def create_user(self, email, username, password= None):
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

    def create_superuser(self, email, username, password=None):

        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

# User custom model
class User(AbstractBaseUser):

    username= models.CharField(max_length=50)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    is_admin = models.BooleanField(default= False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['username']

    objects = Manager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj= None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True

# Function that detects when a product has been modified and sends a email 
# to all the registered users
def price_updated(sender, instance, **kwargs):
    
    queryset = User.objects.filter(is_active=True).values_list('email', flat=True)
    #serializer = UserSerializer(data=queryset)

    subject = 'subject'
    body = 'The product ' + instance.name + ' changed!'
    from_email = 'from_email@test.com'
    recipient_list = list(queryset)
            
    messages = [(subject, body, from_email, [r]) for r in recipient_list]

    send_mass_mail(messages) 

post_save.connect(price_updated, sender = Product)