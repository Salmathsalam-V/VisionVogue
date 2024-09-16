from django.conf import settings
from django.db import models
from Category.models import Category
from django.urls import reverse
from Accounts.models import Account
from django.db.models import Avg, Count
from django.utils.text import slugify
from decimal import Decimal, InvalidOperation
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils import timezone
from datetime import date

class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    features        = models.CharField(max_length=20,default="none",choices=[('polarized', 'Polarized'), ('gradient', 'Gradient'), ('uv protection', 'UV Protection'), ('color changing', 'Color Changing'),('none','None')])
    frame_model     = models.CharField(max_length=20,default="aviator")
    sex             = models.CharField(max_length=20, default="unisex")
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    is_delete       = models.BooleanField(default=False)
    review_count = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2 ,default= 0.00)

    def update_rating(self):
        reviews = self.reviews.all()
        self.review_count = reviews.count()
        self.average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0.00
        self.save()

    def get_url(self):
        return reverse('store:product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)
    def get_first_variation(self):
        return self.variation_set.filter(is_active=True).order_by('created_date').first()

    def get_stock(self):
        variation = self.get_first_variation()
        if variation:
            return variation.stock
        return 0  # Default if no variation exists

    def get_price(self):
        variation = self.get_first_variation()
        if variation:
            return variation.price
        return self.price  # Default to the product's base price if no variation exists

    def get_offer_price(self):
        variation = self.get_first_variation()
        if variation:
            return variation.offer_price
        return self.offer_price  # Default to the product's base offer price if no variation exists

    def get_total(self):
        return sum(item.sub_total() for item in self.cartitem_set.all())

    def get_grand_total(self):
        return self.offer_price() + 100 

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)


variation_category_choice = (
    ('color', 'color'),
)

class Variation(models.Model):
    product            = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value    = models.CharField(max_length=100)
    images             = ProcessedImageField(
                         upload_to='photos/products',
                         processors=[ResizeToFill(300, 200)],  # Crop and resize to 300x200
                         format='JPEG',
                         options={'quality': 90} , blank=True,null=True
                         )
    
    stock              = models.IntegerField(default=0)
    price              = models.IntegerField(default=1000)
    offer_price        = models.DecimalField(max_digits=10, decimal_places=2 ,default= 0.00)

    is_active          = models.BooleanField(default=True)
    created_date       = models.DateTimeField(auto_now=True)
    
    objects = VariationManager()
    
    def __str__(self):
        return self.variation_value

class ImageGallery(models.Model):
    variation = models.ForeignKey(Variation, related_name='gallery_images', on_delete=models.CASCADE,blank=True)
    images = models.ImageField(upload_to='photos/variation_gallery',blank=True, null=True)

    def __str__(self):
        return f"Image for {self.variation.variation_value} ({self.variation.product.product_name})"
    
class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="review")
    review = models.TextField()
    rating = models.IntegerField()

    def update_rating(self):
        reviews = self.reviews.all()
        self.review_count = reviews.count()
        self.average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0.00
        self.save()
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_rating()

# # offer
# class ProductOffer(models.Model):
#     product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='discount')
#     discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 10 for 10%
#     start_date = models.DateField(default=timezone.now)
#     end_date = models.DateField()

#     def __str__(self):
#         return f"{self.product} - {self.discount_percentage}%"

# class CategoryOffer(models.Model):
#     category = models.OneToOneField(Category, on_delete=models.CASCADE)
#     discount_percentage = models.PositiveIntegerField()
#     start_date = models.DateField(default=timezone.now)
#     end_date = models.DateField()

#     def __str__(self):
#         return f"{self.category} - {self.discount_percentage}%"



class Wishlist(models.Model):
    user        = models.ForeignKey(Account, on_delete=models.CASCADE)
    variation    = models.ManyToManyField(Variation)
