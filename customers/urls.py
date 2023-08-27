from django.urls import path

from customers.apps import CustomersConfig
from customers.views import CustomerListView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView

app_name = CustomersConfig.name

urlpatterns = [
    path('customers/', CustomerListView.as_view(), name='list'),
    path('customers/add/', CustomerCreateView.as_view(), name='add'),
    path('customers/edit/<int:pk>/', CustomerUpdateView.as_view(), name='update'),
    path('customers/delete/<int:pk>/', CustomerDeleteView.as_view(), name='delete'),
]