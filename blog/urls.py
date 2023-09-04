from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogDetailView

app_name = BlogConfig.name

urlpatterns = [
    path('blog/', BlogListView.as_view(), name='list'),
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
]