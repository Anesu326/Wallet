from django.urls import path
from . import views

urlpatterns = [path('register/',
                    views.register_view,
                    name='register'),
                path('login/',
                     views.login_view,
                     name='login'),
                path('dashboard/', views.dashboard_view,
                     name='dashboard'),
                path('history/',
                     views.transaction_history_view,
                     name='transaction_history'),
                path('logout/',
                     views.logout_view,
                     name='logout'),]