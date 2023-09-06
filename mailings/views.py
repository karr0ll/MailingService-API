import datetime

import pytz
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from mailings.forms import MailingCreateForm, MailingSettingsUpdateForm, MailingSettingsManagerUpdateForm
from mailings.mailings_service import send_mail_and_log
from mailings.models import Mailing, Logs


class MailingListView(LoginRequiredMixin, ListView):
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
    model = Mailing
    form_class = MailingCreateForm
    extra_context = {'title': 'Создать рассылку'}
    success_url = reverse_lazy('mailings:list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:register')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user.id)
        return queryset

    def form_valid(self, form):
        current_time = datetime.datetime.now().replace(tzinfo=pytz.UTC)
        status = ''
        error_message = ''
        user = form.instance.user = self.request.user

        if form.is_valid():
            customers = form.cleaned_data['customers']
            new_mailing = form.save()
            for customer in customers:
                new_mailing.customers.add(customer.pk)
            new_mailing.save()
            send_mail_and_log(
                new_mailing=new_mailing,
                current_time=current_time,
                customers=customers,
                user=user,
                status=status,
                error_message=error_message
            )
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    login_url = 'users:register'
    redirect_field_name = 'register'
    model = Mailing

    def get_title(self):
        return self.object.title

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(id=self.kwargs.get('pk'))
        return queryset


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = 'users:register'
    redirect_field_name = 'register'

    model = Mailing
    form_class = MailingCreateForm
    extra_context = {'title': 'Редактировать рассылку'}

    def has_permission(self):
        object_ = self.get_object()
        user = self.request.user
        if object_.user != user:
            return object_
        else:
            raise PermissionError('Редактировать рассылки может только пользователь')

    def get_success_url(self):
        return reverse('mailings:list')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user.id)
        return queryset

    def get_form(self, form_class=MailingCreateForm):
        return super().get_form(form_class=MailingCreateForm)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'users:register'
    redirect_filed_name = 'register'

    model = Mailing
    extra_context = {'title': 'Удалить рассылку'}
    success_url = reverse_lazy('mailings:list')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user.id)
        return queryset


class MailingSettingsUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'users:register'
    redirect_filed_name = 'register'

    permission_required = ('mailings.change_mailings', 'mailings.view_mailings')

    model = Mailing
    form_class = MailingSettingsUpdateForm
    extra_context = {'title': 'Настроить рассылку'}
    success_url = reverse_lazy('mailings:list')

    def get_template_names(self):
        template_name = 'mailings/mailing_settings_form.html'
        return template_name

    def has_permission(self):
        object_ = self.get_object()
        user = self.request.user
        if object_.user == user or (user.is_staff and user.has_perms(self.permission_required)):
            return object_
        else:
            raise PermissionError('Редактировать настройки может только пользователь или менеджер')

    def get_form_class(self):
        user = self.request.user
        if user.is_staff and user.has_perms(self.permission_required):
            return MailingSettingsManagerUpdateForm
        else:
            return MailingSettingsUpdateForm

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('mailings.update'):
            return queryset
        else:
            queryset = queryset.filter(user=self.request.user.id)
            return queryset

    def form_valid(self, form):
        # TODO: поправить баг с перезаписью пользователя
        current_time = datetime.datetime.now().replace(tzinfo=pytz.UTC)
        status = ''
        error_message = ''
        user = form.instance.user = self.request.user
        print(user)
        if form.has_changed():
            if user.is_staff:
                updated_settings = form.save()
                updated_settings.save()
            else:
                customers = form.cleaned_data['customers']
                updated_settings = form.save()
                for customer in customers:
                    updated_settings.customers.add(customer.pk)
                updated_settings.save()

                send_mail_and_log(
                    new_mailing=updated_settings,
                    current_time=current_time,
                    customers=customers,
                    user=user,
                    status=status,
                    error_message=error_message
                )
        return super().form_valid(form)


class MailingLogsListView(LoginRequiredMixin, ListView):
    login_url = 'users:register'
    redirect_filed_name = 'register'

    model = Logs
    extra_context = {"title": "Логи рассылок"}

    def get_template_names(self):
        template_name = 'mailings/mailing_logs_list.html'
        return template_name

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user.id)
        return queryset
