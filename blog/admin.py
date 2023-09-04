from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'thumbnail', 'creation_date', 'views_count')
    search_fields = ('title', 'creation_date')
