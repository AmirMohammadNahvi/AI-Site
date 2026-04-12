from django.conf import settings
from django.db import models
from django.utils.text import slugify

from core.models import TimeStampedModel


class BlogAuthor(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="blog_author_profile")
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="blog/authors/", blank=True, null=True)
    x_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "نویسنده"
        verbose_name_plural = "نویسندگان"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class BlogCategory(TimeStampedModel):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class BlogPost(TimeStampedModel):
    DRAFT = "draft"
    PUBLISHED = "published"
    STATUS_CHOICES = [
        (DRAFT, "پیش‌نویس"),
        (PUBLISHED, "منتشر شده"),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    author = models.ForeignKey(BlogAuthor, on_delete=models.PROTECT, related_name="posts")
    categories = models.ManyToManyField(BlogCategory, related_name="posts", blank=True)
    cover_image = models.ImageField(upload_to="blog/posts/", blank=True, null=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    seo_description = models.CharField(max_length=320, blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=DRAFT)
    published_at = models.DateTimeField(blank=True, null=True)
    reading_time_minutes = models.PositiveIntegerField(default=5)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
