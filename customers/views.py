from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from customers.forms import CustomerCreateForm
from customers.models import Customer


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    login_url = 'users:login'

    extra_context = {"title": "Клиенты"}


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerCreateForm
    # fields = ('first_name', 'last_name', 'email', 'comment')
    extra_context = {'title': 'Добавить клиента'}
    success_url = reverse_lazy('customers:list_customers')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        user = self.request.user
        context_data['user'] = user
        return context_data

    def form_valid(self, form):
        if form.is_valid():
            user = self.request.user # a1
            new_customer = form.save() # p1
            new_customer.owner.add(user)

            return super().form_valid(form)


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerCreateForm
    extra_context = {'title': 'Редактировать клиента'}

    def get_success_url(self):
        return reverse('customers:list_customers')


class CustomerDeleteView(DeleteView):
    model = Customer
    extra_context = {'title': 'Удалить клиента'}
    success_url = reverse_lazy('customers:list_customers')