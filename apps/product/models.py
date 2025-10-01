from django.db import models
from apps.sklad.models import Venue, Client, Reservation
# Create your models here.


class Product(models.Model):
    venue = models.ForeignKey(
        Venue, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    purchase_price = models.DecimalField(
        max_digits=10, decimal_places=2)  # закупочная
    sell_price = models.DecimalField(
        max_digits=10, decimal_places=2)      # продажная
    sku = models.CharField(max_length=100, blank=True, null=True)

    def margin(self):
        return self.sell_price - self.purchase_price

    def __str__(self):
        return f"{self.name} ({self.venue.name})"


class InventoryItem(models.Model):
    venue = models.ForeignKey(
        Venue, on_delete=models.CASCADE, related_name='inventory')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='inventory_items')
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('venue', 'product')

    def __str__(self):
        return f"{self.product.name} — {self.quantity}"


class Order(models.Model):
    STATUS = (('pending', 'pending'), ('completed',
              'completed'), ('cancelled', 'cancelled'))
    venue = models.ForeignKey(
        Venue, on_delete=models.CASCADE, related_name='orders')
    client = models.ForeignKey(
        Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    items = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(
        max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    comment = models.TextField(blank=True)

    def recalc_total(self):
        total = sum(
            [oi.quantity * oi.unit_price for oi in self.order_items.all()])
        self.total_price = total
        self.save(update_fields=['total_price'])


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2)  # snapshot of sell_price


class ManagerNotification(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    reservation = models.ForeignKey(
        Reservation, on_delete=models.SET_NULL, null=True, blank=True)
    # info, warning, critical
    level = models.CharField(max_length=20, default='info')

    def __str__(self):
        return f"{self.level} {self.message[:60]}"
