from rest_framework import serializers
from .models import Booking, Product, Client, Order, OrderItem

class BookingSerializer(serializers.ModelSerializer):
    room = serializers.StringRelatedField()
    class Meta:
        model = Booking
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class ClientSerializer(serializers.ModelSerializer):
    total_visits = serializers.SerializerMethodField()
    total_spent = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ["id", "name", "phone_number", "total_visits", "total_spent"]

    def get_total_visits(self, obj):
        return obj.total_visits()

    def get_total_spent(self, obj):
        return obj.total_spent()

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "total_price"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_price = serializers.ReadOnlyField()
    class Meta:
        model = Order
        fields = ["id", "client", "room", "created_at", "total_price", "items"]
