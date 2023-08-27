from django.urls import path

from mailings.views import MailingListView, MailingCreateView, MailingUpdateView, MailingDetailView, MailingDeleteView
from users.apps import UsersConfig
from users.service_users import generate_new_password
from users.views import LoginView, LogoutView, UserProfileView, RegisterView, \
    UserConfirmEmailView, EmailConfirmationSentView, EmailConfirmedView, \
    EmailConfirmationFailedView, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='list'),
    path('add/', MailingCreateView.as_view(), name='add'),
    path('edit/<int:pk>/', MailingUpdateView.as_view(), name='update'),
    path('<int:pk>/', MailingDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='delete')
]
