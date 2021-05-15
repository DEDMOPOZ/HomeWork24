from django.db import models
from django.utils.timezone import now


class Author(models.Model):
    name = models.CharField("Author's Name", max_length=100)
    email = models.EmailField("Author's Email", max_length=100)

    def __str__(self):
        return self.name


class Subscriber(models.Model):
    class Meta:
        unique_together = ["email_to", "author_id"]
    email_to = models.EmailField("Subscriber's Email", max_length=100)
    author_id = models.ForeignKey("Author", on_delete=models.CASCADE)

    def __str__(self):
        return self.email_to


class Post(models.Model):
    title = models.CharField("Title", max_length=100)
    description = models.CharField("Description", max_length=100)
    content = models.TextField("Text")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=now)

    def __str__(self):
        return self.title


class Comments(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField("Comment")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return self.post


class Logger(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    time_execution = models.FloatField("time_exec")
    path = models.CharField("path", max_length=100)
    utm = models.CharField("utm", max_length=100)
    ip = models.GenericIPAddressField()

    def __str__(self):
        return self.created


class Book(models.Model):
    title = models.CharField("Book title", max_length=250)
    author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name="books")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField("Category", max_length=250)

    def __str__(self):
        return self.title


class ContactUs(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=250)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
