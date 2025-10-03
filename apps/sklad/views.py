from rest_framework import viewsets
from django.views.generic import TemplateView

from .models import Booking, Product, Client, Order
from .serializers import BookingSerializer, ProductSerializer, ClientSerializer, OrderSerializer
from .permissions import IsAdmin, IsManagerOrAdmin
# --- Pages ---
class ChessboardPage(TemplateView):
    template_name = "banya_chessboard.html"

class StoragePage(TemplateView):
    template_name = "banya_storage.html"

class ClientsPage(TemplateView):
    template_name = "banya_clients.html"

class ShopPage(TemplateView):
    template_name = "banya_shop.html"

class ChartsPage(TemplateView):
    template_name = "banya_charts.html"

# --- API ---
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsManagerOrAdmin]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdmin]

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAdmin]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsManagerOrAdmin]  # менеджеры и админы