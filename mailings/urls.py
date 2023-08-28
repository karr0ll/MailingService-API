from django.urls import path

from mailings.apps import MailingsConfig
from mailings.views import MailingListView, MailingCreateView, MailingUpdateView, MailingDetailView, MailingDeleteView


app_name = MailingsConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='list'),
    path('add/', MailingCreateView.as_view(), name='add'),
    path('edit/<int:pk>/', MailingUpdateView.as_view(), name='update'),
    path('<int:pk>/', MailingDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='delete')
]
