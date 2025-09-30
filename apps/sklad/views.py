from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.dateparse import parse_datetime
from .models import Reservation

@api_view(['POST'])
@permission_classes([AllowAny])  # или ограничьте токеном
def create_reservation(request):
    data = request.data
    r = Reservation.objects.create(
        name=data.get('name'),
        people=int(data.get('people', 0)),
        requested_time=parse_datetime(data.get('requested_time')),
        phone=data.get('phone'),
        source=data.get('source', 'salebot'),
        idempotency_key=data.get('idempotency_key')
    )
    return Response({"ok": True, "reservation_id": r.id})