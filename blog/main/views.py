from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, View

from .authors_services import authors, delete_all_authors, new_author
from .books_services import books
from .categories_services import categories
from .form import CommentForm, ContactUsForm, PostForm, SubscribeForm
from .models import Author, ContactUs, Post
from .post_services import post_all, post_find
from .subsribers_services import sub_all


class PostListView(ListView):
    queryset = post_all()
    template_name = "main/posts.html"


def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = PostForm()
    context = {
        "form": form,
    }
    return render(request, "main/post_create.html", context=context)


def post_show(request, post_id):
    post = post_find(post_id)
    comments = post.comments.all()

    new_comment = None

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect(request.META.get("HTTP_REFERER"))
    else:
        form = CommentForm()
    context = {
        "form": form,
        "post": post,
        "comments": comments,
        "new_comment": new_comment,
    }
    return render(request, "main/post_show.html", context=context)


def post_update(request, post_id):
    pst = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = PostForm(instance=pst, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = PostForm(instance=pst)
    context = {
        "form": form,
    }
    return render(request, "main/post_update.html", context=context)


class PostsXLSX(View):
    filename = "posts_all_list.xlsx"

    def get(self, request, *args, **kwargs):
        import xlsxwriter
        import io

        output = io.BytesIO()

        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        for row_num, post in enumerate(Post.objects.all()):
            worksheet.write(row_num, 0, post.title)
            worksheet.write(row_num, 1, post.description)

        workbook.close()

        output.seek(0)

        response = HttpResponse(
            output,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        response["Content-Disposition"] = "attachment; filename=%s" % self.filename

        return response


def authors_new(request):
    new_author()
    return redirect("authors_all")


def authors_all(request):
    all_authors = authors().prefetch_related("books")
    return render(request, "main/authors.html", {"title": "Authors", "authors": all_authors})


def authors_sub(request):
    subscribe_success = False
    # email_to = request.POST.get("email_to")
    # author_id = request.POST.get("author_id")

    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            subscribe_success = True
    else:
        form = SubscribeForm()

    if subscribe_success:
        # author = Author.objects.get(id=author_id)
        # send_email(email_to, author.name)
        return redirect("subscribers_all")

    context = {
        "form": form,
    }
    return render(request, "main/authors_subscribe.html", context=context)


def authors_del_all(request):
    delete_all_authors()
    return redirect("authors_all")


def books_all(request):
    all_books = books().only("id", "title", "author__name", "category__title").select_related("author", "category")
    return render(request, "main/books.html", {"title": "Books", "books": all_books})


def categories_all(request):
    all_categories = categories().prefetch_related("books")
    return render(request, "main/categories.html", {"title": "Categories", "categories": all_categories})


def subscribers_all(request):
    return render(request, "main/subscribers.html", {"title": "Subscribers", "subscribers": sub_all()})


def api_posts(request):
    all_posts = post_all()
    posts_list = list(all_posts.values())
    return JsonResponse(posts_list, safe=False)


def api_post_show(request, post_id):
    post = post_find(post_id)
    data = {
        "post_title": post.title,
        "post_description": post.description,
        "post_content": post.content
    }
    return JsonResponse(data, safe=False)


def api_author_subscribe(request):
    author_id = request.GET.get("author_id")
    email_to = request.GET.get("email_to")
    data = {"author_id": author_id, "email_to": email_to}
    return JsonResponse(data, safe=False)


def api_subscribers_all(request):
    all_subs = sub_all()
    subs_list = list(all_subs.values())
    return JsonResponse(subs_list, safe=False)


def api_authors_all(request):
    all_authors = authors()
    authors_list = list(all_authors.values())
    return JsonResponse(authors_list, safe=False)


def api_authors_new(request):
    new_author()
    author = Author.objects.last()
    data = {
        "author_id": author.id,
        "author_name": author.name,
        "author_email": author.email
    }
    return JsonResponse(data, safe=False)


class CreateContactUsView(CreateView):
    success_url = reverse_lazy("home_page")
    model = ContactUs
    form_class = ContactUsForm


class ContactUsListView(ListView):
    queryset = ContactUs.objects.all()
    template_name = "main/contact_us_all.html"
