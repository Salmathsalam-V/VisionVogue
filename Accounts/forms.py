from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model 
from .models import Account, Address
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter first name", "class": "form-control"}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter last name", "class": "form-control"}))
    email=forms.CharField(widget=forms.EmailInput(attrs={"placeholder": "Enter email-address", "class": "form-control"}))
    username=forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter email-username", "class": "form-control"}))
    password1=forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Enter password", "class": "form-control"}))
    password2=forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"placeholder": "Confirm password", "class": "form-control"}))
    
    class Meta:
        model = get_user_model()
        fields = ["first_name","last_name","email", "username", "password1", "password2"]

class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("New password and confirm password do not match.")
        
        return cleaned_data
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'phone', 'address_line_1', 'address_line_2', 'country', 'state', 'city']

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ChangePassword(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label="Current Password")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangePassword, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not self.user.check_password(password):
            raise ValidationError("Current password is incorrect.")
        return password

    def clean_new_password(self):
        new_password = self.cleaned_data.get("new_password")

        # Validate the new password using Django's built-in validators
        try:
            validate_password(new_password, self.user)
        except ValidationError as e:
            raise ValidationError(e.messages)

        return new_password

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get("confirm_password")
        new_password = self.cleaned_data.get("new_password")
        if confirm_password != new_password:
            raise ValidationError("New password and confirm password do not match.")
        return confirm_password

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data