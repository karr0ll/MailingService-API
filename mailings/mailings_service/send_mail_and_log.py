import smtplib

from django.conf import settings
from django.core.mail import send_mail

from mailings.models import Logs


def send_mail_and_log(**kwargs):
    new_mailing = kwargs.get('new_mailing')
    current_time = kwargs.get('current_time')
    customers = kwargs.get('customers')
    user = kwargs.get('user')
    status = kwargs.get('status')
    error_message = kwargs.get('error_message')

    if new_mailing.status == 'enabled' and new_mailing.start_time <= current_time:
        try:
            send_mail(
                subject=new_mailing.subject,
                message=new_mailing.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[customer.email for customer in customers],
                fail_silently=False
            )
            status = 'Удачно'
            error_message = ''
        except smtplib.SMTPException as e:
            status = 'Ошибка'
            if 'authentication failed' in str(e):
                error_message = 'Ошибка аутентификации в почтовом сервисе'
        finally:
            Logs.objects.create(
                user=user,
                last_attempt_time=current_time,
                status=status,
                mailing=new_mailing,
                error_message=error_message
            )