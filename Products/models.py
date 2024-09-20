from django.db import models
from Auth.models import User
from Auth.models import UserType
# Create your models here.
from django.utils.translation import gettext_lazy as _
class UserType(models.TextChoices):
    SELLER = 'Seller', _('Seller')
    BUYER = 'Buyer', _('Buyer')
# Product model
class Product(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=50)
    stripe_price_id = models.CharField(max_length=100)  # CharField is better for Stripe IDs
    stripe_product_id = models.CharField(max_length=100)
    # seller = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': UserType.Seller.value})  # FK to User (Seller)
    seller=models.ForeignKey(User,on_delete=models.CASCADE,choices=UserType.choices)
    image = models.ImageField(upload_to="uploads/")
    description = models.TextField()

    def __str__(self):
        return self.name