from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.sklad import views as sk_views
from apps.product import views
from apps.users import views as us_views

api_urlpatterns = [
    path('webhook/salebot/', views.webhook_salebot, name='webhook_salebot'),
    path('timeslots/', sk_views.TimeSlotListCreate.as_view(), name='timeslots'),
    path('reservations/', sk_views.ReservationList.as_view(), name='reservations'),
    path('reservations/<int:pk>/', sk_views.ReservationDetail.as_view(),
         name='reservation_detail'),
    path('inventory/', views.InventoryListCreate.as_view(), name='inventory'),
    path('clients/', sk_views.ClientsList.as_view(), name='clients'),
    path('notifications/', views.NotificationsList.as_view(), name='notifications'),
]

view_urlpatterns = [
    path("register/", us_views.register_user, name="register"),
    path("login/", us_views.login_user, name="login"),
    path("logout/", us_views.logout_user, name="logout"),
    path("dashboard/", us_views.dashboard, name="dashboard"),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_urlpatterns)),
    path('', include(view_urlpatterns)),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
