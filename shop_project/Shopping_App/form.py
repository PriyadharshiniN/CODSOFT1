from pyexpat import model
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms
 
class CustomUserForm(UserCreationForm):
  username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter User Name'}))
  email=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Email Address'}))
  password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Password'}))
  password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Confirm Password'}))
  class Meta:
    model=User
    fields=['username','email','password1','password2']
    


class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16, required=True)
    expiry_date = forms.CharField(max_length=5, required=True)  
    cvv = forms.CharField(max_length=3, required=True)


class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderView
        fields = ['product', 'product_qty']


class QuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1,label='Quantity')
