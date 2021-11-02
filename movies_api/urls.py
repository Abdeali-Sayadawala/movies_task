from django.contrib import admin
from django.urls import path, include
from .views import search_title, search

urlpatterns = [
    path('search-title/', search_title),
    path('search/', search),
]