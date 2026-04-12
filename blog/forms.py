from django import forms

from .models import BlogAuthor, BlogCategory, BlogPost


class BlogAuthorForm(forms.ModelForm):
    class Meta:
        model = BlogAuthor
        fields = ["name", "slug", "bio", "avatar", "x_url", "linkedin_url", "is_active"]


class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogCategory
        fields = ["name", "slug", "description", "is_active"]


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            "title",
            "slug",
            "author",
            "categories",
            "cover_image",
            "excerpt",
            "content",
            "seo_description",
            "status",
            "published_at",
            "reading_time_minutes",
            "is_featured",
        ]
