from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView

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
        context['mailing_count'] = Mailing.objects.all().count()
        context['enabled_mailing'] = Mailing.objects.filter(status='enabled').count()
        # context['unique_users'] = Mailing.objects
        # print(Customer.mailing_set.all())
        return context

