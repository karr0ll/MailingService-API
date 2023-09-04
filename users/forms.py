from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

from users.models import User


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserForm(UserCreationForm):
    """
    Форма регистрации пользователя
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = (
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
        )


class UserProfileForm(UserChangeForm):
    """
    Форма обновления данных пользователя
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
        )
        exclude = ('password',)


class UserManagerForm(UserProfileForm):
    """
    Форма настройки активации пользователя для менеджера
    """
    email = forms.CharField(disabled=True, label="Email")
    first_name = forms.CharField(disabled=True, label="Имя")
    last_name = forms.CharField(disabled=True, label="Фамилия")

    class Meta:
        model = User

        exclude = (
            'last_login',
            'is_superuser',
            'groups',
            'user_permissions',
            'is_staff',
            'date_joined',
            'verification_code',
            'password',
            'password1',
            'password2',
            )





