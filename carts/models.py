from django.db import models
from Store . models import Product, Variation
from VisionVogue import settings
 

# Create your models here.
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 10 for 10%
    active = models.BooleanField(default=True)
    minimum_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Minimum amount to apply the coupon
    usage_limit = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.code

class UserCoupon(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    usage_count = models.IntegerField(default=0)  # Number of times the user has used the coupon

    class Meta:
        unique_together = ('user', 'coupon')

    def __str__(self):
        return f"{self.user.username} - {self.coupon.code}"

class Cart(models.Model):
    user_id    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default=1)
    cart_id    = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)
    discount   = models.IntegerField(default=0)
    grand_total = models.IntegerField(default=0)
    coupons    = models.ManyToManyField(Coupon, blank=True)  # Updated to ManyToManyField

    def __unicode__(self):
        return self.cart_id

    def get_discount(self):
        total_discount = 0
        if self.coupons.exists():
            for coupon in self.coupons.all():
                total_discount += (coupon.discount / 100) * self.get_total()
        return total_discount

    def get_total(self):
        return sum(item.sub_total() for item in self.cartitem_set.all())

    def get_grand_total(self):
        return self.get_total() + 100 - self.get_discount()
    
    

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE ,null=True)
    sub_total  = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)

    class Meta:
        unique_together = ('product', 'cart', 'variation') 

    def sub_total(self):
        # Check if variation exists
        if self.variation:
            return self.variation.offer_price * self.quantity
        return 0


    def __unicode__(self):
        return self.product

