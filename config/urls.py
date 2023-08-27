from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('users/', include('users.urls', namespace='users')),
    path('customers/', include('customers.urls', namespace='customers')),
    path('mailings/', include('mailings.urls', namespace='mailings'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
