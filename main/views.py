import datetime
import smtplib

import pytz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from config import settings
from mailings import models
from mailings.mailings_service import send_mailing
from mailings.models import Mailing, Logs


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = 'users:login'
    template_name = 'main/index.html'
    context = {
        'title': 'Главная страница'
    }

