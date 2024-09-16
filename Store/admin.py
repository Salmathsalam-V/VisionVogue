from django.contrib import admin
from . models import ImageGallery, Product, Variation
# Register your models here.

class ImageGalleryInline(admin.TabularInline):
    model = ImageGallery
    extra = 2  # Number of empty image fields to display

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name',  'category', 'modified_date', 'is_available','is_delete','features','frame_model','sex')
    prepopulated_fields = {'slug': ('product_name',)}

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active', 'images', 'stock','price','offer_price')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')
    inlines = [ImageGalleryInline]
    
admin.site.register(Variation, VariationAdmin)
admin.site.register(Product, ProductAdmin)
