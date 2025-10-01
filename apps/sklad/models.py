from django.db import models
from apps.users.models import User

class Venue(models.Model):
    TYPE_CHOICES = (('banya','Баня'), ('cafe','Кафе'))
    name = models.CharField(max_length=200)
    venue_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    description = models.TextField(blank=True)
    timezone = models.CharField(max_length=50, default='Asia/Bishkek')

    def __str__(self):
        return f"{self.name} ({self.get_venue_type_display()})"

class TimeSlot(models.Model):
    """
    Описывает страницу со свободными местами.
    Один слот = время начала + вместимость для конкретного заведения (например, 18:00-20:00)
    """
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='timeslots')
    start = models.DateTimeField()
    end = models.DateTimeField()
    capacity = models.IntegerField(default=10)  # общее количество мест
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['start']
        unique_together = ('venue','start','end')

    def reserved_count(self):
        return self.reservations.filter(status__in=['confirmed','arrived']).count()

    def free_places(self):
        return max(0, self.capacity - self.reserved_count())

    def __str__(self):
        return f"{self.venue.name} {self.start.isoformat()} ({self.free_places()}/{self.capacity})"

class Client(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def visits_count(self):
        return self.orders.filter(status='completed').count() + self.reservations.filter(status='arrived').count()

    def total_spent(self, period_start=None, period_end=None):
        qs = self.orders.filter(status='completed')
        if period_start:
            qs = qs.filter(created_at__gte=period_start)
        if period_end:
            qs = qs.filter(created_at__lte=period_end)
        return qs.aggregate(total=models.Sum('total_price'))['total'] or 0

    def __str__(self):
        return f"{self.name or self.phone} ({self.phone})"

class Reservation(models.Model):
    STATUS = (
        ('new','new'),
        ('confirmed','confirmed'),
        ('cancelled','cancelled'),
        ('arrived','arrived'),
        ('no_show','no_show'),
    )
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='reservations')
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50)
    people = models.IntegerField(default=1)
    requested_time = models.DateTimeField()  # точное время, которое прислал клиент
    source = models.CharField(max_length=100, default='salebot')
    status = models.CharField(max_length=20, choices=STATUS, default='new')
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    idempotency_key = models.CharField(max_length=200, blank=True, null=True, unique=True)

    flagged = models.BooleanField(default=False)  # флаг от менеджера (или автоматический)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Можно здесь или сигналом проверять visits_count и создавать уведомление

    def __str__(self):
        return f"{self.venue.name} {self.requested_time} {self.name or self.phone}"
