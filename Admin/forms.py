from django import forms
from Category . models import Category
from Orders.models import Order
from Store . models import Product
from carts.models import Coupon
from Store . models import ImageGallery
from decimal import Decimal
from Store . models import Variation, ImageGallery
from django.forms.models import inlineformset_factory

class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = ['product', 'variation_category', 'variation_value', 'is_active', 'stock', 'price', 'offer_price','images']
    def __init__(self, *args, **kwargs):
        super(VariationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'  # Special class for checkbox
            else:
                field.widget.attrs['class'] = 'form-control' 


# Formset for handling multiple images related to a variation
ImageGalleryFormSet = inlineformset_factory(
    Variation,  # Parent model
    ImageGallery,  # Related model
    fields=('images',),  # Only include the image field
    extra=3,  # Number of empty image fields to display
    can_delete=True,  # Allow deletion of images
    widgets={
        'images': forms.FileInput(attrs={'class': 'form-control'}),
    }
)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['brand_name','description','is_delete','brand_logo','discount_percentage']
    widgets = {
            'brand_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'is_delete': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'brand_logo': forms.FileInput(attrs={'class': 'form-control'}),
            'discount_percentage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Discount %'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'  # Special class for checkbox
            else:
                field.widget.attrs['class'] = 'form-control' 


class ProductForm(forms.ModelForm):
    FRAME_MODEL_CHOICES = [
        ('aviator', 'Aviator'),
        ('clubmaster', 'Clubmaster'),
        ('oval', 'Oval'),
        ('cat style', 'Cat Style'),
    ]
    
    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('unisex', 'Unisex')
    ]

    frame_model = forms.ChoiceField(choices=FRAME_MODEL_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(choices=SEX_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    is_delete = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    is_available = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'frame_model', 'sex', 'description', 'features', 'is_available', 'is_delete']
        widgets = {
            'images': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'image2': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'image3': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter the category field to exclude deleted categories
        self.fields['category'].queryset = Category.objects.filter(is_delete=False)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'  # Special class for checkbox
            else:
                field.widget.attrs['class'] = 'form-control' 


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=Order.STATUS),
        }
    

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount', 'active','minimum_amount','usage_limit']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter the category field to exclude deleted categories
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'  # Special class for checkbox
            else:
                field.widget.attrs['class'] = 'form-control' 
