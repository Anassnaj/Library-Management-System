from rest_framework import serializers
from .models import Book, LibraryUser, Transaction

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'published_date', 'number_of_copies_available']

class LibraryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryUser
        fields = ['id', 'username', 'date_of_membership', 'is_active_member']
    
    def validate_username(self, value):
        if LibraryUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username must be unique.")
        return value
    
    def validate_email(self, value):
        if LibraryUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email must be unique.")
        return value

class TransactionSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'user_username', 'book_title', 'book', 'checkout_date', 'return_date']
    
    # Add validation for ensuring one copy of a book can only be checked out by a user
    def validate_book(self, value):
        if value.copies_available <= 0:
            raise serializers.ValidationError("This book is not available for checkout.")
        return value

    def create(self, validated_data):
        # Decrease the available copies of the book when creating a checkout transaction
        book = validated_data['book']
        if book.copies_available > 0:
            book.copies_available -= 1
            book.save()

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # When the book is returned, increase available copies
        if 'return_date' in validated_data and validated_data['return_date'] is not None:
            book = instance.book
            book.copies_available += 1
            book.save()

        return super().update(instance, validated_data)
