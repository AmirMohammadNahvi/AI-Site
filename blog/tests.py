from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import BlogAuthor, BlogPost


class BlogViewsTests(TestCase):
    def setUp(self):
        self.author = BlogAuthor.objects.create(name="نویسنده تست", slug="author-test")
        self.post = BlogPost.objects.create(
            title="مقاله تست",
            slug="test-post",
            author=self.author,
            content="محتوای تست",
            status=BlogPost.PUBLISHED,
            published_at=timezone.now(),
        )

    def test_blog_list_and_detail(self):
        response = self.client.get(reverse("blog:list"))
        self.assertContains(response, "مقاله تست")
        detail = self.client.get(reverse("blog:detail", args=[self.post.slug]))
        self.assertContains(detail, "محتوای تست")
