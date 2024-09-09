from django.db import models
from django.contrib.auth import get_user_model
from VisionVogue import settings

class Image(models.Model):
    file = models.ImageField(upload_to='photos/imagecrop')
    uploaded = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return str(self.pk)

User = get_user_model()

class SalesReport(models.Model):
    PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom Date Range'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default=1)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2)
    total_orders = models.PositiveIntegerField()
    total_discount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.period.capitalize()} Report ({self.start_date} - {self.end_date})'

    class Meta:
        ordering = ['-created_at']