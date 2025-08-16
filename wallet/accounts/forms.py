from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

# Registration form
class RegisterForm(forms.ModelForm):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email', 'password']

# Login form
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email')

# Send money form
class SendMoneyForm(forms.Form):
    receiver_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Name',        
    }))
    receiver_email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
        'min': '10'
    }))
    amount = forms.DecimalField(min_value=10, max_value=10000, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Amount',
        'min': '10'
    }))
    currency = forms.ChoiceField(choices=[('GBP', 'GBP'), ('ZAR', 'ZAR')], widget=forms.Select(attrs={
        'class': 'form-control'        
    }))
