from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, SendMoneyForm
from .models import Profile, Transaction
from django.contrib.auth.models import User
from decimal import Decimal, ROUND_HALF_UP

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['email'],
                                            email = form.cleaned_data['email'], 
                                            password=form.cleaned_data['password'])
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
            receiver_name = form.cleaned_data['receiver_name']
            receiver_email = form.cleaned_data['receiver_email']
            fx_rates = {'GBP':Decimal(0.78), 'ZAR':Decimal(18.2)}
            fees = {'GBP':Decimal(0.10), 'ZAR':Decimal(0.20)}
            fee = amount * fees[currency]
            final = (amount - fee) * fx_rates[currency]
            final = final.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            fx_rates = fx_rates[currency].quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            fee = fee.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            transaction = Transaction.objects.create(user=request.user,
                                                     receiver_name = receiver_name,
                                                     receiver_email = receiver_email,
                                                     amount_usd=amount,
                                                     currency=currency,
                                                     fee=fee,
                                                     final_amount=final,
                                                     fx_rate=fx_rates,)
            result = {
                'receiver_name': receiver_name,
                'receiver_email': receiver_email,
                'amount': amount,
                'fee':fee,
                'rate':fx_rates,
                'final':final,
                'currency':currency,
                'timestamp': transaction.timestamp,
            }
        else:
            form = SendMoneyForm()
        return render(request, 'accounts/dashboard.html', {'form':form, 'result':result})

@login_required
def transactions_view(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'accounts/transactions.html',{'transactions':transactions})
# Create your views here.
