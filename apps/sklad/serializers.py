from rest_framework import serializers, generics
from .models import Venue, TimeSlot, Client, Reservation
from rest_framework.permissions import IsAuthenticated


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = '__all__'


class TimeSlotSerializer(serializers.ModelSerializer):
    free_places = serializers.IntegerField(
        source='free_places', read_only=True)

    class Meta:
        model = TimeSlot
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    visits = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'name', 'phone', 'created_at', 'visits']

    def get_visits(self, obj):
        return obj.visits_count()


class ReservationSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['flagged', 'created_at', 'client']

    def create(self, validated_data):
        # idempotency
        idk = validated_data.get('idempotency_key')
        if idk:
            exists = Reservation.objects.filter(idempotency_key=idk).first()
            if exists:
                return exists
        # find timeslot if exact match
        timeslot = validated_data.pop('timeslot', None)
        r = Reservation.objects.create(**validated_data)
        return r


class ClientsList(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
