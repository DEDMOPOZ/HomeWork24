from faker import Faker

from .models import Author


def authors():
    all_authors = Author.objects.all()
    return all_authors


def new_author():
    faker = Faker()
    Author(name=faker.name(), email=faker.email()).save()
    return


def delete_all_authors():
    Author.objects.all().delete()
    return
