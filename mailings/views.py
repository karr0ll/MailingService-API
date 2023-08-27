from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from mailings.models import Mailing


class MailingListView(ListView):
    model = Mailing
    extra_context = {"title": "Рассылки"}


class MailingCreateView(CreateView):
    model = Mailing
    fields = ('subject', 'body', 'customers')
    extra_context = {'title': 'Создать рассылку'}
    success_url = reverse_lazy('mailings:list')


class MailingDetailView(DetailView):
    model = Mailing

    def get_title(self):
        return self.object.title


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ('subject', 'body')
    extra_context = {'title': 'Редактировать рассылку'}

    def get_success_url(self):
        return reverse('mailings:list')


class MailingDeleteView(DeleteView):
    model = Mailing
    extra_context = {'title': 'Удалить рассылку'}
    success_url = reverse_lazy('mailings:list')