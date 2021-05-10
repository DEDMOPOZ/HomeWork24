from django.shortcuts import get_object_or_404

from .models import Post


def post_all():
    all_posts = Post.objects.all()
    return all_posts


def post_find(post_id: int) -> Post:
    post = get_object_or_404(Post, pk=post_id)
    return post
