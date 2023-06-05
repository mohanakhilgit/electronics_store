from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Product


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", 'placeholder': 'Enter your username'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control", 'placeholder': 'Enter your password'
            }
        )
    )


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", 'placeholder': 'Enter your name'
            }
        )
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", 'placeholder': 'Enter your email'
            }
        )
    )
    password1 = forms.CharField(
        max_length=100, widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Enter a valid password'
            }
        )
    )
    password2 = forms.CharField(
        max_length=100,  widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Confirm Password', 'data-toggle': 'password'
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProductForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", 'placeholder': 'Enter Product Name'
            }
        )
    )

    price = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control", 'placeholder': 'Enter the Price'
            }
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Product Description",
                "rows": 5,
            }
        )
    )

    image = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control-file"
            }
        )
    )

    stock = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = Product
        fields = ('name', 'price', 'image', 'stock')


class ProductUpdateForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", 'placeholder': 'Enter Product Name'
            }
        )
    )

    price = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control", 'placeholder': 'Enter the Price'
            }
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Product Description",
                "rows": 5,
            }
        )
    )

    image = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control-file"
            }
        )
    )


    stock = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = Product
        fields = '__all__'