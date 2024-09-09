from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.

class Category(models.Model):
    brand_name   = models.CharField(max_length=50, unique=True)
    slug         = models.SlugField(max_length=100, unique=True)
    description  = models.TextField(max_length=255, blank=True)
    brand_logo = ProcessedImageField(
        upload_to='photos/categories',
        processors=[ResizeToFill(300, 200)],  # Crop and resize to 300x200
        format='JPEG',
        options={'quality': 90}
    )
    is_delete    = models.BooleanField(default=False)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2,default=0)  # e.g., 10 for 10%

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def get_url(self):
        return reverse('store:products_by_category', args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.brand_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.brand_name
    
    def get_discounted_price(self,price):
        discount_percentage = self.discount_percentage or 0
        discount_amount = (price * discount_percentage) / 100
        return price - discount_amount
