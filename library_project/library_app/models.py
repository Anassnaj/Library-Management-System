from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Book(models.Model):
    title = models.CharField(max_length=200)  # The title of the book.
    author = models.CharField(max_length=100)  # The author of the book.
    isbn = models.CharField(max_length=13, unique=True)  # Unique ISBN number.
    published_date = models.DateField()  # The date the book was published.
    copies_available = models.PositiveIntegerField()  # Number of available copies.

    def __str__(self):
        return self.title

class LibraryUser(AbstractUser):
    date_of_membership = models.DateField(auto_now_add=True)  # Membership date.
    is_active = models.BooleanField(default=True)  # Indicates if the user is active.
    
    groups = models.ManyToManyField(
        Group,
        related_name="library_users",  # Avoids conflicts with the default User model
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="library_users",  # Avoids conflicts with the default User model
        blank=True
    )

class Transaction(models.Model):
    user = models.ForeignKey('LibraryUser', on_delete=models.CASCADE)  # User who borrowed the book.
    book = models.ForeignKey('Book', on_delete=models.CASCADE)  # Book being borrowed.
    checkout_date = models.DateTimeField(auto_now_add=True)  # Date of checkout.
    return_date = models.DateTimeField(null=True, blank=True)  # Date of return.

    def __str__(self):
        return f"{self.user.username} checked out {self.book.title} on {self.checkout_date}" 
