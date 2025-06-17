# potions/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.potion_calculator_view, name='potion_calculator'),
]