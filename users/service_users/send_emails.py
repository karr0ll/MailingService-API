from django.conf import settings
from django.core.mail import send_mail


def send_verification_link(activation_url, user_email):
    send_mail(
        subject='Подтверждение адреса почты',
        message=f'Пожалуйста, '
                f'перейдите по следующей ссылке, '
                f'чтобы подтвердить свой адрес электронной почты: '
                f'http://127.0.0.1:8000{activation_url}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email]
    )


def send_new_password(new_password, user_email):
    send_mail(
        subject='Смена пароля',
        message=f'Вы сгенерировали новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email]
    )
