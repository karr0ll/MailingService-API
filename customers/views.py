from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from customers.forms import CustomerCreateForm
from customers.models import Customer


class CustomerListView(LoginRequiredMixin, ListView):
    """Контроллер вывода списка всех клиентов"""
    model = Customer
    login_url = 'users:login'

    extra_context = {"title": "Клиенты"}


class CustomerCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания клиента"""

    model = Customer
    form_class = CustomerCreateForm
    extra_context = {'title': 'Добавить клиента'}
    success_url = reverse_lazy('customers:list')

    def get_context_data(self, **kwargs):
        """Метод получения контекста"""
        context_data = super().get_context_data()
        user = self.request.user
        context_data['user'] = user
        return context_data

    def form_valid(self, form):
        """Метод получения данных из формы"""
        if form.is_valid():
            user = self.request.user
            new_customer = form.save()
            new_customer.owner.add(user)
            new_customer.save()
            return super().form_valid(form)


class CustomerUpdateView(UpdateView):
    """Контроллер обновления клиента"""
    model = Customer
    form_class = CustomerCreateForm
    extra_context = {'title': 'Редактировать клиента'}

    def get_success_url(self):
        """Метод переадресации после создания пользователя"""
        return reverse('customers:list')


class CustomerDeleteView(DeleteView):
    """Контроллер удаления клиента"""
    model = Customer
    extra_context = {'title': 'Удалить клиента'}
    success_url = reverse_lazy('customers:list')