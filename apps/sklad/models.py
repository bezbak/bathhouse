from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ("booked", "Забронировано"),
        ("in_progress", "В процессе"),
        ("done", "Завершено"),
        ("canceled", "Отменено"),
    ]

    client_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="booked")
    people_count = models.PositiveIntegerField(default=1)
    arrival_time = models.DateTimeField()
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.client_name} ({self.arrival_time})"
    
class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    supplier = models.CharField(max_length=150)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_unit = models.CharField(
        max_length=20,
        choices=[("piece", "за штуку"), ("kg", "за кг"), ("g", "за грамм")],
        default="piece"
    )
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
class Client(models.Model):
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20, unique=True)

    def total_visits(self):
        return Booking.objects.filter(phone_number=self.phone_number, status="done").count()

    def total_spent(self):
        orders = Order.objects.filter(client=self)
        return sum(o.total_price for o in orders)

    def __str__(self):
        return f"{self.name} ({self.phone_number})"
    
class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return sum([i.total_price for i in self.items.all()])

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.quantity * self.product.sale_price