from django.contrib import admin

from .models import Author, Comments, Logger, Post, Subscriber

admin.site.register(Author)
admin.site.register(Logger)
admin.site.register(Post)
admin.site.register(Subscriber)


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post_id", "created")
