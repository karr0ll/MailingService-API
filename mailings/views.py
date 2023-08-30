from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from mailings.forms import MailingCreateForm
from mailings.models import Mailing


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    login_url = 'users:login'

    extra_context = {"title": "Рассылки"}


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingCreateForm
    extra_context = {'title': 'Создать рассылку'}
    success_url = reverse_lazy('mailings:list')

    def form_valid(self, form):
        if form.is_valid():
            customers = form.cleaned_data['customers']
            form.instance.user = self.request.user
            new_mailing = form.save()
            for customer in customers:
                new_mailing.customers.add(customer.pk)
            new_mailing.save()
            return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def get_title(self):
        return self.object.title


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingCreateForm
    extra_context = {'title': 'Редактировать рассылку'}

    def get_success_url(self):
        return reverse('mailings:list')


class MailingDeleteView(DeleteView):
    model = Mailing
    extra_context = {'title': 'Удалить рассылку'}
    success_url = reverse_lazy('mailings:list')
