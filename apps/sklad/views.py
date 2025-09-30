# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.dateparse import parse_datetime
from rest_framework import status
from .models import Reservation

SALEBOT_TOKEN = "05cf9804c4349f66ba410767621a1029"

@api_view(["POST"])
def create_reservation(request):
    # Проверка токена
    auth_header = request.headers.get("Authorization")
    if auth_header != f"Token {SALEBOT_TOKEN}":
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    data = request.data

    # Проверка idempotency_key (чтобы не было дублей)
    if Reservation.objects.filter(idempotency_key=data.get("idempotency_key")).exists():
        return Response({"ok": True, "status": "duplicate"})

    r = Reservation.objects.create(
        name=data.get("name"),
        people=int(data.get("people") or 0),
        requested_time=parse_datetime(data.get("requested_time")),
        phone=data.get("phone"),
        source=data.get("source", "salebot"),
        idempotency_key=data.get("idempotency_key")
    )
    return Response({"ok": True, "reservation_id": r.id})