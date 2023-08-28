from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from mailings.forms import MailingCreateForm
from mailings.models import Mailing


class MailingListView(ListView):
    model = Mailing
    extra_context = {"title": "Рассылки"}


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingCreateForm
    extra_context = {'title': 'Создать рассылку'}
    success_url = reverse_lazy('mailings:list')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        user = self.request.user
        context_data['user'] = user
        return context_data

    def form_valid(self, form):
        if form.is_valid():
            user = self.request.user
            new_mailing = form.save() # p1
            new_mailing.customer.owner = user
            print(new_mailing.customer)
            return super().form_valid(form)


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