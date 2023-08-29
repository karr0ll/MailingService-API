from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.shortcuts import redirect, resolve_url
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from users.forms import CustomAuthenticationForm, UserForm, UserProfileForm
from users.models import User
from users.service_users import code_generator, send_verification_link, password_generator, send_new_password


class LoginView(BaseLoginView):
    template_name = 'users/login.html'
    form_class = CustomAuthenticationForm


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        generated_code = code_generator(6)
        user = form.save()
        user.is_active = False
        user.verification_code = generated_code

        verification_code = str(generated_code) + str(user.pk)
        activation_url = self.request.build_absolute_uri(
            reverse_lazy(
                'users:verify_email', kwargs={
                    'verification_code': verification_code
                }
            )
        )
        try:
            send_verification_link(activation_url, user.email)  # TODO:добавить обработку исключения
            user.save()
        except SMTPException as e:
            pass

        return redirect('users:verification_link_sent')


class UserConfirmEmailView(View):

    def get(self, request, verification_code):
        uid = int(verification_code[6:])
        code = verification_code[:6]
        try:
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and code == user.verification_code:
            user.is_active = True
            user.verification_code = ""
            user.save()
            return redirect(reverse_lazy('users:email_verified'))
        else:
            return redirect(reverse_lazy('users:verification_failed'))


class EmailConfirmationSentView(TemplateView):
    template_name = 'users/verification_link_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Подтверждение почты'
        return context


class EmailConfirmedView(TemplateView):
    template_name = 'users/email_verified.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Подтверждение почты'
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = 'users/verification_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Подтверждение почты'
        return context


class UserProfileView(LoginRequiredMixin, ListView):
    login_url = 'users:login'

    model = User
    extra_context = {"title": "Профиль"}


    def get_template_names(self):
        template_name = 'users/profile.html'
        return template_name

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        user = self.request.user
        context_data['user'] = user
        return context_data

class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    extra_context = {'title': 'Профиль'}
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        return self.request.user
