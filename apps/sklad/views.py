from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from .serializers import TimeSlotSerializer, ReservationSerializer, ClientSerializer
from .models import Reservation, TimeSlot, Client


class TimeSlotListCreate(generics.ListCreateAPIView):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    permission_classes = [IsAuthenticated]


class ReservationList(generics.ListAPIView):
    queryset = Reservation.objects.select_related(
        'client', 'venue', 'timeslot').all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'phone', 'client__phone']


class ReservationDetail(generics.RetrieveUpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]


class ClientsList(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
