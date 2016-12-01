from django import forms
from .models import Product, UserProfile
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('userLogo',)


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'



