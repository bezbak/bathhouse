from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status, generics, filters
from apps.sklad.models import TimeSlot
from .models import Venue, InventoryItem, Product, Order, ManagerNotification
from .serializers import InventoryItemSerializer, ProductSerializer, OrderSerializer, ManagerNotificationSerializer
from django.utils.dateparse import parse_datetime
from django.db.models import Sum
from django.conf import settings
from django.shortcuts import get_object_or_404


SALEBOT_TOKEN = "05cf9804c4349f66ba410767621a1029"
AMO_TOKEN = "ВАШ_AMO_TOKEN_IF_NEEDED"


@api_view(['POST'])
@permission_classes([AllowAny])
def webhook_salebot(request):
    # Поддерживаем SaleBot и amo crm webhooks. Проверка заголовка
    data = request.data
    print(data)
    # ожидаем: name, people, requested_time, phone, source, idempotency_key, venue_id (опционально)
    phone = data.get('phone')
    name = data.get('name') or ''
    people = int(data.get('people') or 1)
    requested_time = None
    if data.get('requested_time'):
        try:
            requested_time = parse_datetime(data.get('requested_time'))
        except:
            requested_time = None

    venue = None
    if data.get('venue_id'):
        venue = get_object_or_404(Venue, id=data.get('venue_id'))
    else:
        # выбираем дефолт (первый)
        venue = Venue.objects.first()

    # попытка установить timeslot: ищем слот охватывающий requested_time
    timeslot = None
    if requested_time:
        timeslot = TimeSlot.objects.filter(
            venue=venue, start__lte=requested_time, end__gte=requested_time).first()

    payload = {
        'venue': venue,
        'timeslot': timeslot,
        'name': name,
        'phone': phone,
        'people': people,
        'requested_time': requested_time or timezone.now(),
        'source': data.get('source', 'salebot'),
        'note': data.get('note', ''),
        'idempotency_key': data.get('idempotency_key')
    }
    # create reservation
    # создадим Client если не существует
    from apps.sklad.models import Client, Reservation
    client, _ = Client.objects.get_or_create(
        phone=phone, defaults={'name': name})
    r = Reservation.objects.create(
        venue=venue,
        timeslot=timeslot,
        client=client,
        name=name,
        phone=phone,
        people=people,
        requested_time=payload['requested_time'],
        source=payload['source'],
        note=payload['note'],
        idempotency_key=payload['idempotency_key']
    )
    # возвращаем id и флаг (если нет мест)
    free = timeslot.free_places() if timeslot else None
    return Response({'ok': True, 'reservation_id': r.id, 'timeslot_free': free})

# CRUD примеры


class InventoryListCreate(generics.ListCreateAPIView):
    queryset = InventoryItem.objects.select_related('product', 'venue').all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]


class NotificationsList(generics.ListAPIView):
    queryset = ManagerNotification.objects.filter(is_read=False)
    serializer_class = ManagerNotificationSerializer
    permission_classes = [IsAuthenticated]


class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class OrderListCreate(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
