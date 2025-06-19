# potions/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.potion_calculator_view, name='potion_calculator'),
    path('profit-api/', views.potion_profit_api, name='potion_profit_api'),
]