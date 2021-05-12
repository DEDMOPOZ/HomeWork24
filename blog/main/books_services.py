from .models import Book


def books():
    all_books = Book.objects.all()
    return all_books
