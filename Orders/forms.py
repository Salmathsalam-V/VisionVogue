from django import forms
from Accounts . models import Address
from Orders.models import Payment

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city']



# PAYMENT_METHOD_CHOICES = [
#     ('COD', 'Cash on Delivery'),
#     ('Razorpay', 'Razorpay'),
# ]

# class PaymentForm(forms.ModelForm):
#     payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES, widget=forms.RadioSelect)

#     class Meta:
#         model = Payment
#         fields = ['payment_method']