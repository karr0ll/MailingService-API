from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.shortcuts import redirect, resolve_url, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from users.forms import CustomAuthenticationForm, UserForm, UserProfileForm, UserManagerForm
from users.models import User
from users.service_users import code_generator, send_verification_link, password_generator, send_new_password


class LoginView(BaseLoginView):
    template_name = 'users/login.html'
    form_class = CustomAuthenticationForm


class LogoutView(BaseLogoutView):
    template_name = 'users/login.html'


class RegisterView(CreateView):
    """
    Контроллер регистрации пользователя
    """
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'
    extra_context = {
        'title': 'Регистрация'}

    def form_valid(self, form):
        """Метод получения данных формы"""
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
            send_verification_link(activation_url, user.email)
            user.save()
            return redirect('users:verification_link_sent')
        except SMTPException as e:
            user.delete()
            return redirect('users:sending_error')


class EmailSendingError(TemplateView):
    """Контроллер вывода страницы в случае неудачной отправки письма"""
    template_name = 'users/email_sending_failed.html'
    extra_context = {
        'title': 'Ошибка'}


class UserConfirmEmailView(View):
    """Контрллер подтверждения регистрации по ссылке"""

    def get(self, request, verification_code):
        """Метод проверки валидность ссылки потдверждения регистрации"""
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
    """Контроллер вывода страницы уведомления об отправке письма"""
    template_name = 'users/verification_link_sent.html'
    extra_context = {
        'title': 'Подтверждение почты'}


class EmailConfirmedView(TemplateView):
    """Контроллер вывода страницы подтвреждения регистрации"""
    template_name = 'users/email_verified.html'
    extra_context = {
        'title': 'Подтверждение почты'}


class EmailConfirmationFailedView(TemplateView):
    """Контроллер вывода страницы подтвреждения регистрации"""

    template_name = 'users/verification_failed.html'
    extra_context = {
        'title': 'Подтверждение почты'}


class UserProfileView(LoginRequiredMixin, ListView):
    """Контроллер отображения профиля пользователя"""
    login_url = 'users:login'
    template_name = 'users/profile.html'
    model = User
    extra_context = {"title": "Профиль"}

    def get_context_data(self, *args, **kwargs):
        """Методы передачи в контекст объекта пользователя"""
        context_data = super().get_context_data(*args, **kwargs)
        user = self.request.user
        context_data['user'] = user
        return context_data


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер обновления данных пользователя
    """
    model = User
    success_url = reverse_lazy('users:profile')
    extra_context = {
        'title': 'Профиль'
    }
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        return self.request.user


class UsersListView(LoginRequiredMixin, ListView):
    """Контроллер вывода списка всех пользователей для менеджера"""
    login_url = 'users:register'
    redirect_field_name = 'register'

    model = User
    extra_context = {'title': 'Пользователи'}
    template_name = 'users/users_list.html'

    def get_queryset(self):
        """Метод получения данных из базы"""
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset


class UsersManagerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер управления пользователями для менеджера (активация/деактивация)"""
    login_url = 'users:register'
    redirect_field_name = 'register'
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:list')

    permission_required = ('users.change_users', 'users.view_users')

    model = User
    extra_context = {'title': 'Активация пользователя'}

    def has_permission(self):
        """Метод проверки прав пользователя"""
        object_ = self.get_object()
        user = self.request.user
        if user.is_staff and user.has_perms(self.permission_required):
            return object_
        else:
            raise PermissionError('Редактировать статус пользователя может только менеджер')

    def get_form_class(self):
        """Метод вывода формы управления пользователем для менеджера"""
        user = self.request.user
        if user.is_staff and user.has_perms(self.permission_required):
            return UserManagerForm

    def form_valid(self, form):
        """Метод получения данных из формы"""
        if form.has_changed():
            user = get_object_or_404(User, id=self.kwargs['pk'])
            if user.is_active:
                user.is_active = False
            else:
                user.is_active = True

            user.save()
        return super().form_valid(form)


