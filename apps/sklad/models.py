from django.db import models

class Reservation(models.Model):
    name = models.CharField(max_length=255)
    people = models.IntegerField(default=1)
    requested_time = models.DateTimeField()
    phone = models.CharField(max_length=20)
    source = models.CharField(max_length=50)
    idempotency_key = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name} - {self.requested_time}"