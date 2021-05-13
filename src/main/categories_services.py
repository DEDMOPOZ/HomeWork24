from .models import Category


def categories():
    all_categories = Category.objects.all()
    return all_categories
