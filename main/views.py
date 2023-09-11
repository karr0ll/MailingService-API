import random

from django.core.cache import cache

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from blog.models import Blog
from customers.models import Customer
from mailings.models import Mailing


class IndexView(LoginRequiredMixin, TemplateView):
    """Контрлллер вывода главной страницы"""
    login_url = 'users:login'
    template_name = 'main/index.html'
    extra_context = {
        'title': 'Главная страница'
    }

    def get_context_data(self, *args, **kwargs):
        """Метод получения контекста"""
        user = self.request.user
        if self.request.method == 'GET':
            if settings.CACHE_ENABLED:
                key = f'cached_statistics'
                cached_context = cache.get(key)
                if cached_context is None:
                    context = super().get_context_data(*args, **kwargs)
                    if not user.is_staff:
                        context['mailing_count'] = Mailing.objects.filter(user=user).count()
                        context['enabled_mailing'] = Mailing.objects.filter(user=user).filter(status='enabled').count()
                        context['unique_users'] = Customer.objects.filter(owner=user).distinct('email').count()
                    else:
                        context['mailing_count'] = Mailing.objects.all().count()
                        context['enabled_mailing'] = Mailing.objects.all().filter(status='enabled').count()
                        context['unique_users'] = Customer.objects.all().distinct('email').count()
                        main_page_context = {
                            'mailing_count': context['mailing_count'],
                            'enabled_mailing': context['enabled_mailing'],
                            'unique_users': context['unique_users']
                        }
                        cache.set(key, main_page_context)
                        all_blog_posts = Blog.objects.all()
                        random_posts = random.sample(list(all_blog_posts), 3)
                        context['three_random_posts'] = random_posts
                    return context
                else:
                    context = super().get_context_data(*args, **kwargs)
                    context['mailing_count'] = cached_context['mailing_count']
                    context['enabled_mailing'] = cached_context['enabled_mailing']
                    context['unique_users'] = cached_context['unique_users']
                    all_blog_posts = Blog.objects.all()
                    random_posts = random.sample(list(all_blog_posts), 3)
                    context['three_random_posts'] = random_posts
                return context
