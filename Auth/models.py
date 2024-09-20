from django.db import models
from django.utils.translation import gettext_lazy as _
# from Products.models import Customer

# Use Django's TextChoices for UserType
class UserType(models.TextChoices):
    SELLER = 'Seller', _('Seller')
    BUYER = 'Buyer', _('Buyer')

# Abstract class for common fields
class AbstractClass(models.Model):
    id = models.AutoField(primary_key=True)  # Use lowercase 'id'
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True

# Customer model linked to User
class Customer(AbstractClass):
    email = models.EmailField()
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='customer_profile')  # Use related_name

    def __str__(self):
        return self.name

# User model
class User(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.BUYER  # Default value for the user_type
    )

    # Link User to one Customer
    customer = models.OneToOneField('Customer', on_delete=models.CASCADE, null=True, blank=True, related_name='user_profile')  # Use related_name to avoid clash

    def __str__(self):
        return self.username

# OTP model
class OTP(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    otp = models.CharField(max_length=4)

    def __str__(self):
        return f"OTP for {self.email}"
