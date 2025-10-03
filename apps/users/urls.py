from django.urls import path
from .views import HomePage, LoginPage, BanyaPage, CafePage, LoginView, LogoutView

urlpatterns = [
    # Pages
    path("", HomePage.as_view(), name="home"),
    path("login/", LoginPage.as_view(), name="login_page"),
    path("banya/", BanyaPage.as_view(), name="banya_page"),
    path("cafe/", CafePage.as_view(), name="cafe_page"),
    path("api/v1/auth/login/", LoginView.as_view(), name="api_login"),
    path("api/v1/auth/logout/", LogoutView.as_view(), name="api_logout"),
]
