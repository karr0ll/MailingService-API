from django.shortcuts import redirect
from django.urls import reverse

from users.service_users import password_generator, send_new_password


def generate_new_password(request):
    new_password = password_generator(size=12)
    send_new_password(new_password, request.user.email)
    if request.user.is_authenticated:
        request.user.set_password(new_password)
        request.user.save()
        return redirect(reverse('users:profile'))