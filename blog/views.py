from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import BlogAuthor, BlogCategory, BlogPost


def post_list(request):
    query = request.GET.get("q", "").strip()
    posts = BlogPost.objects.filter(status=BlogPost.PUBLISHED).select_related("author").prefetch_related("categories")
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(excerpt__icontains=query) | Q(content__icontains=query))
    return render(request, "blog/post_list.html", {"posts": posts, "query": query})


def post_detail(request, slug):
    post = get_object_or_404(
        BlogPost.objects.select_related("author").prefetch_related("categories"),
        slug=slug,
        status=BlogPost.PUBLISHED,
    )
    related_posts = BlogPost.objects.filter(status=BlogPost.PUBLISHED).exclude(id=post.id)[:3]
    return render(request, "blog/post_detail.html", {"post": post, "related_posts": related_posts})


def category_detail(request, slug):
    category = get_object_or_404(BlogCategory, slug=slug, is_active=True)
    posts = category.posts.filter(status=BlogPost.PUBLISHED)
    return render(request, "blog/category_detail.html", {"category": category, "posts": posts})


def author_detail(request, slug):
    author = get_object_or_404(BlogAuthor, slug=slug, is_active=True)
    posts = author.posts.filter(status=BlogPost.PUBLISHED)
    return render(request, "blog/author_detail.html", {"author": author, "posts": posts})
