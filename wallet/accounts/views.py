from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, SendMoneyForm
from .models import Profile, Transaction
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.shortcuts import redirect
from decimal import Decimal, ROUND_HALF_UP
from .utils import get_fx_rates
from django.utils import timezone

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['name'],
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
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'accounts/login.html', {'error':'Invalid credentials.'})
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by('-timestamp')
    fx_rates = get_fx_rates()
    result = None
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')
    paginator = Paginator(transactions, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    result = None
    form = SendMoneyForm()

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
            result = None
        context = {
            'result':{
                'amount': amount,
                'fee': fee,
                'final_amount': final,
                'receiver_name': receiver_name,
                'receiver_email': receiver_email,
                'currency': currency,
                'rate': fx_rates,
                'timestamp': timezone.now(),
                
            },
            
            'page_obj': page_obj,
            'transactions': transactions,
        }
        form = SendMoneyForm()
        return render(request, 'accounts/dashboard.html', context)
    return render(request, 'accounts/dashboard.html',{
        'page_obj':page_obj,
        'form': form       
    })
            
    # else:
                
    # return render(request, 'accounts/dashboard.html', {'form':form, 'result':result, 'page_obj':page_obj,})

@login_required
def transaction_history_view(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'accounts/history.html', {'transactions': transactions})