from rest_framework.test import APITestCase
from ..models import User, Product

class TestUserModel(APITestCase):
    # Testing the creation of a regular user
    def test_create_user(self):
        user = User.objects.create_user("test@test.com", "test", "test")
        self.assertIsInstance(user, User)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_superuser)

    # Testing the creation of a super user
    def test_create_super_user(self):
        user = User.objects.create_superuser("test@test.com", "test", "test")
        self.assertIsInstance(user, User)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_admin)
        self.assertTrue(user.is_superuser)

    # Testing the raised error when there is no email
    def test_raises_error_if_not_email(self):
        self.assertRaises(ValueError, User.objects.create_user, username = "test@test.com", email= "", password= "test")
        self.assertRaisesMessage(ValueError, "Users must have a email")

    # Testing the raised error when there is no username
    def test_raises_error_if_not_username(self):
        self.assertRaises(ValueError, User.objects.create_user, username = "", email= "test", password= "test")
        self.assertRaisesMessage(ValueError, "Users must have an username")

class TestProductModel(APITestCase):
    
    # Testing product creation
    def test_create_product(self):
        product = Product.objects.create(name = "product name", price = 1000, brand = "product brand", availability = "IN_STOCK", avg_rating = "5.0")
        self.assertIsInstance(product, Product)
