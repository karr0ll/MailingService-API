from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogDetailView

app_name = BlogConfig.name

urlpatterns = [
    path('blog/', cache_page(180)(BlogListView.as_view()), name='list'),
    path('post/<int:pk>/', cache_page(180)(BlogDetailView.as_view()), name='post_detail'),
]