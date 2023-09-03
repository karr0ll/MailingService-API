import datetime
import smtplib

import pytz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from mailings.forms import MailingCreateForm, MailingSettingsUpdateForm
from mailings.mailings_service import send_mailing
from mailings.models import Mailing, Logs


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    login_url = 'users:login'

    extra_context = {"title": "Рассылки"}

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user.id)
        return queryset


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingCreateForm
    extra_context = {'title': 'Создать рассылку'}
    success_url = reverse_lazy('mailings:list')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user.id)
        return queryset

    def form_valid(self, form):
        current_time = datetime.datetime.now().replace(tzinfo=pytz.UTC)

        if form.is_valid():
            customers = form.cleaned_data['customers']
            form.instance.user = self.request.user
            new_mailing = form.save()
            for customer in customers:
                new_mailing.customers.add(customer.pk)
            new_mailing.save()

            if new_mailing.status == 'enabled' and new_mailing.start_time <= current_time:
                try:
                    send_mailing(
                        subject=new_mailing.subject,
                        message=new_mailing.body,
                        recipients=customers
                    )
                    status = 'ok'
                    error_message = None
                except smtplib.SMTPException as e:
                    status = 'failed'
                    error_message = e
                finally:
                    Logs.objects.create(
                        user=form.instance.user,
                        last_attempt_time=current_time,
                        status=status,
                        mailing=new_mailing,
                        error_message=error_message
                    )

            return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def get_title(self):
        return self.object.title

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(id=self.kwargs.get('pk'))
        return queryset


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingCreateForm
    extra_context = {'title': 'Редактировать рассылку'}

    def get_success_url(self):
        return reverse('mailings:list')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user.id)
        return queryset

    def get_form(self, form_class=MailingCreateForm):
        return super().get_form(form_class=MailingCreateForm)


class MailingDeleteView(DeleteView):
    model = Mailing
    extra_context = {'title': 'Удалить рассылку'}
    success_url = reverse_lazy('mailings:list')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user.id)
        return queryset


class MailingSettingsUpdateView(UpdateView):
    model = Mailing
    form_class = MailingSettingsUpdateForm
    extra_context = {'title': 'Настроить рассылку'}
    success_url = reverse_lazy('mailings:list')

    def get_template_names(self):
        template_name = 'mailings/mailing_settings_form.html'
        return template_name

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user.id)
        return queryset

    def form_valid(self, form):
        current_time = datetime.datetime.now().replace(tzinfo=pytz.UTC)

        if form.has_changed():
            customers = form.cleaned_data['customers']
            form.instance.user = self.request.user
            new_mailing = form.save()
            for customer in customers:
                new_mailing.customers.add(customer.pk)
            new_mailing.save()

            if new_mailing.status == 'enabled' and new_mailing.start_time <= current_time:
                try:
                    send_mailing(
                        subject=new_mailing.subject,
                        message=new_mailing.body,
                        recipients=customers
                    )
                    status = 'ok'
                    error_message = None
                except smtplib.SMTPException as e:
                    status = 'failed'
                    error_message = e
                finally:
                    Logs.objects.create(
                        user=form.instance.user,
                        last_attempt_time=current_time,
                        status=status,
                        mailing=new_mailing,
                        error_message=error_message
                    )
        return super().form_valid(form)


class MailingLogsListView(LoginRequiredMixin, ListView):
    model = Logs
    login_url = 'users:login'

    extra_context = {"title": "Логи рассылок"}

    def get_template_names(self):
        template_name = 'mailings/mailing_logs_list.html'
        return template_name

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user.id)
        return queryset

    # def get_context_data(self, *args, **kwargs):
    #     context_data = super().get_context_data(*args, **kwargs)
    #     queryset = self.get_queryset()
    #     return context_data