from django.urls import path, include
from rest_framework.routers import DefaultRouter
from library_app.views import BookViewSet, UserViewSet, TransactionViewSet, ReturnBookView, CheckOutBookView

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'users', UserViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    # Add the APIView-based views to the urlpatterns
    path('return-book/', ReturnBookView.as_view(), name='return-book'),
    path('checkout-book/', CheckOutBookView.as_view(), name='checkout-book'),
    
    # Include the router's URLs
    path('', include(router.urls)),
]
