from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.query_params.get('title')
        author = self.request.query_params.get('author')
        isbn = self.request.query_params.get('isbn')
        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__icontains=author)
        if isbn:
            queryset = queryset.filter(isbn=isbn)
        return queryset

from .models import LibraryUser
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = LibraryUser.objects.all()
    serializer_class = UserSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Book, Transaction

class CheckOutBookView(APIView):
    def post(self, request):
        user = request.user
        book_id = request.data.get('book_id')
        book = Book.objects.get(id=book_id)

        if book.copies_available > 0:
            Transaction.objects.create(user=user, book=book)
            book.copies_available -= 1
            book.save()
            return Response({"message": "Book checked out successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "No copies available"}, status=status.HTTP_400_BAD_REQUEST)

class ReturnBookView(APIView):
    def post(self, request):
        user = request.user
        book_id = request.data.get('book_id')
        transaction = Transaction.objects.get(user=user, book_id=book_id, return_date__isnull=True)
        transaction.return_date = timezone.now()
        transaction.save()

        book = transaction.book
        book.copies_available += 1
        book.save()
        return Response({"message": "Book returned successfully"}, status=status.HTTP_200_OK)
