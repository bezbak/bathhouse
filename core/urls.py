from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.sklad.views import create_reservation

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/create_reservation/',
         create_reservation, name='create_reservation')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
