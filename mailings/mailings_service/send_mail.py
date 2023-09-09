from django.core.mail import send_mail

from config import settings


def do_send_mail(**kwargs):

    subject = kwargs.get('subject')
    message = kwargs.get('message')
    recipients = kwargs.get('recipients')
    send_mail(
        subject=f'{subject}',
        message=f'{message}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[recipient.email for recipient in recipients],
        fail_silently=False
    )



