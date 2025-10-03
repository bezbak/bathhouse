from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ChessboardPage, StoragePage, ClientsPage, ShopPage, ChartsPage,
    BookingViewSet, ProductViewSet, ClientViewSet, OrderViewSet
)


router = DefaultRouter()
router.register("api/v1/bookings", BookingViewSet, basename="booking")
router.register("api/v1/products", ProductViewSet, basename="product")
router.register("api/v1/clients", ClientViewSet, basename="client")
router.register("api/v1/orders", OrderViewSet, basename="order")

urlpatterns = [
    # Pages
    path("chessboard/", ChessboardPage.as_view(),
         name="banya_chessboard_page"),
    path("storage/", StoragePage.as_view(), name="banya_storage_page"),
    path("clients/", ClientsPage.as_view(), name="banya_clients_page"),
    path("shop/", ShopPage.as_view(), name="banya_shop_page"),
    path("charts/", ChartsPage.as_view(), name="banya_charts_page"),

]
urlpatterns += router.urls