from django.db import models
from Auth.models import User,Customer
# from Products.models import Customer
class Payment(models.Model):
    Id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # FK to User
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # FK to Customer
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Use DecimalField for monetary values
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment by {self.user.username} of {self.amount}"