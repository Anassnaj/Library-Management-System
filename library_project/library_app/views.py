from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Book, LibraryUser, Transaction
from .serializers import BookSerializer, LibraryUserSerializer, TransactionSerializer

# ViewSet for Book model
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

# ViewSet for LibraryUser model
class LibraryUserViewSet(viewsets.ModelViewSet):
    queryset = LibraryUser.objects.all()
    serializer_class = LibraryUserSerializer

# ViewSet for Transaction model (to handle checkout and return operations)
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        # Handle checkout operation
        book_id = request.data.get('book')
        user_id = request.data.get('user')
        try:
            book = Book.objects.get(id=book_id)
            user = LibraryUser.objects.get(id=user_id)

            if book.copies_available > 0:
                # Create the transaction
                transaction = Transaction.objects.create(
                    user=user,
                    book=book,
                    checkout_date=timezone.now()
                )
                # Update available copies
                book.copies_available -= 1
                book.save()

                return Response({'message': 'Book checked out successfully.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'No copies available.'}, status=status.HTTP_400_BAD_REQUEST)

        except Book.DoesNotExist:
            return Response({'message': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)
        except LibraryUser.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

# View for returning a book
class ReturnBookView(APIView):
    def post(self, request, *args, **kwargs):
        # Handle return operation
        transaction_id = request.data.get('transaction_id')
        try:
            transaction = Transaction.objects.get(id=transaction_id)

            # Mark the book as returned
            transaction.return_date = timezone.now()
            transaction.save()

            # Update the available copies of the book
            transaction.book.copies_available += 1
            transaction.book.save()

            return Response({'message': 'Book returned successfully.'}, status=status.HTTP_200_OK)

        except Transaction.DoesNotExist:
            return Response({'message': 'Transaction not found.'}, status=status.HTTP_404_NOT_FOUND)

# Custom View for checking out a book (if needed for custom API endpoint)
class CheckOutBookView(APIView):
    def post(self, request):
        # Get the current user
        user = request.user
        
        # Get the book_id from the request data
        book_id = request.data.get('book_id')

        # Check if book exists
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if copies are available
        if book.copies_available <= 0:
            return Response({"error": "No copies available for checkout."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new transaction
        transaction = Transaction.objects.create(user=user, book=book, checkout_date=timezone.now())

        # Decrease the available copies of the book
        book.copies_available -= 1
        book.save()

        # Return a success message with the serialized book data
        return Response({
            "message": "Book checked out successfully.",
            "book": BookSerializer(book).data
        }, status=status.HTTP_200_OK)
