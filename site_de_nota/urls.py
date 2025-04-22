"""
URL configuration for site_de_nota project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # URL para o admin
    path('', include('notas.urls')),  # Inclua as URLs do app `notas`
]
