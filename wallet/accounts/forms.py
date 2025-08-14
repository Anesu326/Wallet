from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(forms.ModelForm):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email', 'password']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email')

class SendMoneyForm(forms.Form):
    receiver_name = forms.CharField(max_length=100)
    receiver_email = forms.CharField()
    amount = forms.DecimalField(min_value=10, max_value=10000)
    currency = forms.ChoiceField(choices=[('GBP', 'GBP'), ('ZAR', 'ZAR')])
