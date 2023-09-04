from django.views.generic import ListView, DetailView

from blog.models import Blog


class TitleViewMixin:
    title = ""

    def get_title(self):
        return self.title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_title()
        return context


class BlogListView(ListView):
    model = Blog
    extra_context = {"title": "Блог"}

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter()
        return queryset


class BlogDetailView(TitleViewMixin, DetailView):
    model = Blog

    def get_title(self):
        return self.object.title

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object