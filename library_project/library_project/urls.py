"""
URL configuration for library_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.shortcuts import render
from rest_framework.routers import DefaultRouter
from library_app.views import BookViewSet, UserViewSet, TransactionViewSet, CheckOutBookView, ReturnBookView

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'users', UserViewSet, basename= 'user')
router.register(r'transactions', TransactionViewSet)

def home(request):
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel URL
    path('api/v1/', include(router.urls)),  # API routes with a version prefix
    path('api/v1/return-book/', ReturnBookView.as_view(), name='return-book'),  # API route for returning books
    path('api/v1/checkout-book/', CheckOutBookView.as_view(), name='checkout-book'),  # API route for checking out books
    path('', home, name='home'),
]
