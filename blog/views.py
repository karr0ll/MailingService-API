import django.db.models
from django.views.generic import ListView, DetailView

from blog.models import Blog


class TitleViewMixin:
    """Контроллер получения title"""
    title = ""

    def get_title(self):
        """Метод получения заголовка"""
        return self.title

    def get_context_data(self, **kwargs):
        """Метод получения контекста"""
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_title()
        return context


class BlogListView(ListView):
    """Контроллер вывода всех записей блога"""
    model = Blog
    extra_context = {"title": "Блог"}

    def get_queryset(self):
        """Метод получения данных всех постов"""
        queryset = super().get_queryset()
        queryset = queryset.filter()
        return queryset


class BlogDetailView(TitleViewMixin, DetailView):
    """Контроллер отображения данных об одном посте"""
    model = Blog

    def get_title(self):
        """Метод получения заголовка"""
        return self.object.title

    def get_object(self, queryset=None):
        """Метод добавления просмотров постов"""
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object