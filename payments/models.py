from django.db import models
from accounts.models import CustomUser
from core.models import Product
# Create your models here.
class Transaction(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    transaction_uuid=models.CharField(max_length=200)
    transaction_code=models.CharField(max_length=200)
    status=models.CharField(max_length=200)
    product_code=models.CharField(max_length=200)
    total_amount=models.CharField( max_length=200)
    created_at=models.DateField(auto_now=True)

class Order(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    transaction_uuid=models.CharField(max_length=50)
    total_amount=models.CharField(max_length=200)
    status=models.CharField(max_length=200)
    created_at=models.DateField(auto_now=True)

class OrderItem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    price=models.CharField(max_length=200)
    quantity=models.CharField(max_length=200)
