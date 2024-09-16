from django.db import models
from Accounts . models import Account,Address
from Store . models import Product, Variation
from django.utils import timezone
from datetime import timedelta

from carts.models import Coupon

# Create your models here.
    

class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Shipped', 'Shipped'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    user         = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    address      = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    order_total  = models.FloatField()
    shipping_cost  = models.FloatField(blank=True, default=100)
    status       = models.CharField(max_length=10, choices=STATUS, default='New')
    ip           = models.CharField(blank=True, max_length=20)
    is_ordered   = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    discount_amount = models.FloatField(blank=True, default=0)
    final_amount = models.FloatField(blank=True, default=0)
    coupons    = models.ManyToManyField(Coupon, blank=True) 

class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100) # this is the total amount paid
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id
    

class OrderProduct(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True,default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE ,null=True)
    quantity = models.IntegerField(default=1)    
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name
    
class Return(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True,default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.CharField(max_length=250,null=True)
    status = models.BooleanField(default=False)
