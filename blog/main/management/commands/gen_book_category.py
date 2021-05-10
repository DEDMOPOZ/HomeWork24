from django.core.management import BaseCommand
from faker import Faker
from main.models import Author, Book, Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()
        file = "book genres.txt"
        for _ in range(300):
            Author(name=faker.name(), email=faker.email()).save()

        with open(file, "r") as file:
            for line in file:
                Category(title=line).save()

        for i in range(1000):
            author = Author.objects.order_by("?").last()
            category = Category.objects.order_by("?").last()
            Book(title=f"Title {i}", author=author, category=category).save()
