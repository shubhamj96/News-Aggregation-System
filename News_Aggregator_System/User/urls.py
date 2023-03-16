"""News_Aggregator_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path

from User import views

urlpatterns = [
    path('', views.userLogInCheck, name='u-check'),
    path('u-home/', views.userHomePage, name='homepage'),
    path('signup/', views.userSignUp, name='signup'),
    path('registration/', views.userRegistraion, name='registration'),
    path('discription/<id>', views.userDiscription, name='discription'),
    path('watchlist/', views.userWatchList, name='watchlist'),
    path('addwatchlist/<id>', views.addWatchList, name='addwatchlist'),
    path('showwatchlist/<id>', views.showWatchList, name='showwatchlist'),
    path('u-logout/', views.userLogOut, name='logout'),
    path('u-dashboard/', views.userDashBoard, name='dashboard'),
    path('u-profile/', views.userProfile, name='profile'),
    path('u-account/', views.userAccountSeetings, name='account'),
    path('u-update/', views.userAccountUpdate, name='update'),

#---------------------------****************-------------------------------------------------#
    path('search_result/<ref>/', views.searchResult, name='s-result'),
    path('lang/<l>/<ref>', views.langPreference, name='lang'),
    path('sort/<s>', views.sortNews, name='sort'),
]