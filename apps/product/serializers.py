from rest_framework import serializers
from .models import Product, InventoryItem, Order, OrderItem, ManagerNotification

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class InventoryItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = InventoryItem
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(
        many=True, source='order_items', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class ManagerNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerNotification
        fields = '__all__'
