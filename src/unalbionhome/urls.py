"""
URL configuration for unalbionhome project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from .views import home_view
from animal_artifacts.views import animal_artifacts_view
from account.views import login_signup_view
from fishingbait.views import fishing_profit_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('animal-artifacts/', animal_artifacts_view, name='animal_artifacts'),
    path('accounts/',login_signup_view,name='accounts'),
    path('fishing-bait/', fishing_profit_view, name='fishing_bait'),
    path('potions/', include('potions.urls')),
]
