from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, SendMoneyForm
from .models import Profile
from django.contrib.auth.models import User

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['email'],
                                            email = form.cleaned_data['email'], password=form.cleaned_data['password'])
            user.profile.name = form.cleaned_data['name']
            user.profile.save()
            return redirect('login')
        else:
            form = RegisterForm()
            return render(request, 'accounts/register.html', {'form':form})
        
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
        else:
            form = LoginForm()
            return render(request, 'accounts/login.html', {'form':form})

@login_required
def dashboard_view(request):
    result = None
    if request.method == 'POST':
        form = SendMoneyForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            currency = form.cleaned_data['currency']
            fx_rates = {'GBP':0.78, 'ZAR':18.2}
            fees = 

# Create your views here.
