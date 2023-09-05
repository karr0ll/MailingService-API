import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.views.generic import TemplateView

from blog.models import Blog
from config import settings
from customers.models import Customer
from mailings.models import Mailing


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = 'users:login'
    template_name = 'main/index.html'
    extra_context = {
        'title': 'Главная страница'
    }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = self.request.user
        context['mailing_count'] = Mailing.objects.filter(user=user).count()
        context['enabled_mailing'] = Mailing.objects.filter(user=user).filter(status='enabled').count()
        context['unique_users'] = Customer.objects.filter(owner=user).distinct('email').count()
        all_blog_posts = Blog.objects.all()
        random_posts = random.sample(list(all_blog_posts), 3)
        context['three_random_posts'] = random_posts
        return context

    # def get_context_data(self, *args, **kwargs):  #-> cannot pickle '_io.BufferedReader' object
    #     user = self.request.user
    #     if self.request.method == 'GET':
    #         if settings.CACHE_ENABLED:
    #             key = f'cached_statistics'
    #             context = cache.get(key)
    #             if context is None:
    #                 context = super().get_context_data(*args, **kwargs)
    #                 context['mailing_count'] = Mailing.objects.filter(user=user).count()
    #                 context['enabled_mailing'] = Mailing.objects.filter(user=user).filter(status='enabled').count()
    #                 context['unique_users'] = Customer.objects.filter(owner=user).distinct('email').count()
    #                 cache.set(key, context)
    #             else:
    #                 context = super().get_context_data(*args, **kwargs)
    #                 context['mailing_count'] = Mailing.objects.filter(user=user).count()
    #                 context['enabled_mailing'] = Mailing.objects.filter(user=user).filter(status='enabled').count()
    #                 context['unique_users'] = Customer.objects.filter(owner=user).distinct('email').count()
    #                 all_blog_posts = Blog.objects.all()
    #                 random_posts = random.sample(list(all_blog_posts), 3)
    #                 context['three_random_posts'] = random_posts
    #             return context
