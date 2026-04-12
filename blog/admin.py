from django.contrib import admin

from .models import BlogAuthor, BlogCategory, BlogPost


admin.site.register(BlogAuthor)
admin.site.register(BlogCategory)
admin.site.register(BlogPost)
