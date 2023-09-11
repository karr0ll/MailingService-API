import calendar
from datetime import datetime, timedelta

import pytz
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from mailings.forms import MailingCreateForm, MailingSettingsUpdateForm, MailingSettingsManagerUpdateForm
from mailings.mailings_service import send_mail_and_log
from mailings.models import Mailing, Logs


class MailingListView(LoginRequiredMixin, ListView):
    """Контроллер отображения всех рассылок"""
    model = Mailing
    login_url = 'users:login'

    extra_context = {"title": "Рассылки"}

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('mailings.view_mailings'):
            return queryset
        else:
            queryset = queryset.filter(user=self.request.user.id)
            return queryset


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания рассылки """

    model = Mailing
    form_class = MailingCreateForm
    extra_context = {'title': 'Создать рассылку'}
    success_url = reverse_lazy('mailings:list')

    def dispatch(self, request, *args, **kwargs):
        """Метод передадерсации пользователя, если он не прошел аутентификацию"""
        if not request.user.is_authenticated:
            return redirect('users:register')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Метод получения данных из базы"""
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user.id)
        return queryset

    def form_valid(self, form):
        """Метод получения данных из формы"""
        current_time = datetime.now().replace(tzinfo=pytz.UTC)
        status = ''
        error_message = ''
        form.instance.user = self.request.user

        if form.is_valid():
            customers = form.cleaned_data['customers']
            new_mailing = form.save()
            if new_mailing.start_time > current_time:
                new_mailing.next_attempt = new_mailing.start_time
            else:
                if new_mailing.interval == 'every_minute':
                    new_mailing.next_attempt = new_mailing.start_time + timedelta(minutes=1)

                if new_mailing.interval == 'daily':
                    new_mailing.next_attempt = new_mailing.start_time + timedelta(days=1)

                if new_mailing.interval == 'weekly':
                    new_mailing.next_attempt = new_mailing.start_time + timedelta(days=7)

                if new_mailing.interval == 'monthly':
                    today = datetime.today()
                    days = calendar.monthrange(today.year, today.month)[1]
                    new_mailing.next_attempt = current_time + timedelta(days=days)

                for customer in customers:
                    new_mailing.customers.add(customer.pk)
                new_mailing.save()
                send_mail_and_log(
                    new_mailing=new_mailing,
                    current_time=current_time,
                    customers=customers,
                    user=form.instance.user,
                    status=status,
                    error_message=error_message
                )
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    """Контроллер получения данных одной рассылки """

    login_url = 'users:register'
    redirect_field_name = 'register'
    model = Mailing

    def get_title(self):
        """Метод получения заголовка"""
        return self.object.title

    def get_queryset(self):
        """Метод получения данных из базы"""
        queryset = super().get_queryset()
        queryset = queryset.filter(id=self.kwargs.get('pk'))
        return queryset


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер обновления данных рассылки"""
    login_url = 'users:register'
    redirect_field_name = 'register'

    model = Mailing
    form_class = MailingCreateForm
    extra_context = {'title': 'Редактировать рассылку'}

    def has_permission(self):
        """Метод проверки разрешений пользователя"""
        object_ = self.get_object()
        user = self.request.user
        if object_.user == user:
            return object_
        else:
            raise PermissionError('Редактировать рассылки может только пользователь')

    def get_success_url(self):
        """Метод переадресации пользователя"""
        return reverse('mailings:list')

    def get_queryset(self):
        """Метод получения данных из базы"""
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер удаления рассылки"""
    login_url = 'users:register'
    redirect_filed_name = 'register'

    model = Mailing
    extra_context = {'title': 'Удалить рассылку'}
    success_url = reverse_lazy('mailings:list')

    def get_queryset(self):
        """Метод получения данных из базы"""
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user.id)
        return queryset


class MailingSettingsUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер обновления настроек рассылок"""
    login_url = 'users:register'
    redirect_filed_name = 'register'

    permission_required = ('mailings.change_mailings', 'mailings.view_mailings')

    model = Mailing
    form_class = MailingSettingsUpdateForm
    extra_context = {'title': 'Настроить рассылку'}
    success_url = reverse_lazy('mailings:list')
    template_name = 'mailings/mailing_settings_form.html'

    def has_permission(self):
        """Метод проверки прав пользователя"""
        object_ = self.get_object()
        user = self.request.user
        if object_.user == user or (user.is_staff and user.has_perms(self.permission_required)):
            return object_
        else:
            raise PermissionError('Редактировать настройки может только пользователь или менеджер')

    def get_form_class(self):
        """Метод выбора нужной формы для вывода,в зависимости от типа пользователя"""
        user = self.request.user
        if user.is_staff and user.has_perms(self.permission_required):
            return MailingSettingsManagerUpdateForm
        else:
            return MailingSettingsUpdateForm

    def get_queryset(self):
        """Метод получения данных из базы"""
        queryset = super().get_queryset()
        if self.request.user.has_perm('mailings.update'):
            return queryset
        else:
            queryset = queryset.filter(user=self.request.user.id)
            return queryset

    def form_valid(self, form):
        """ Метод сохранения данных формы и отпправки рассылки"""
        current_time = datetime.now().replace(tzinfo=pytz.UTC)
        status = ''
        error_message = ''
        if form.has_changed():
            if self.request.user.is_staff:
                updated_settings = form.save()
                updated_settings.save()
            else:
                customers = form.cleaned_data['customers']
                updated_settings = form.save()

                if updated_settings.interval == 'every_minute':
                    updated_settings.next_attempt = current_time + timedelta(minutes=1)

                if updated_settings.interval == 'daily':
                    updated_settings.next_attempt = current_time + timedelta(days=1)

                elif updated_settings.interval == 'weekly':
                    updated_settings.next_attempt = current_time + timedelta(days=7)

                if updated_settings.interval == 'monthly':
                    today = datetime.today()
                    days = calendar.monthrange(today.year, today.month)[1]
                    updated_settings.next_attempt = current_time + timedelta(days=days)

                for customer in customers:
                    updated_settings.customers.add(customer.pk)
                updated_settings.save()
                form.instance.user = self.request.user
                send_mail_and_log(
                    new_mailing=updated_settings,
                    current_time=current_time,
                    customers=customers,
                    user=form.instance.user,
                    status=status,
                    error_message=error_message
                )

        return super().form_valid(form)


class MailingLogsListView(LoginRequiredMixin, ListView):
    """Контроллер отображения всех логов"""
    login_url = 'users:register'
    redirect_filed_name = 'register'

    model = Logs
    extra_context = {"title": "Логи рассылок"}
    template_name = 'mailings/mailing_logs_list.html'

    def get_queryset(self):
        """Метод получения данных из базы"""
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user.id)
        else:
            queryset = queryset.all()
        return queryset
