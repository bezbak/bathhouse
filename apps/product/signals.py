from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ManagerNotification
from apps.sklad.models import Reservation, Client


@receiver(post_save, sender=Reservation)
def reservation_post_create(sender, instance, created, **kwargs):
    if not created:
        return
    # создаём/находим клиента по телефону
    client, _ = Client.objects.get_or_create(
        phone=instance.phone, defaults={'name': instance.name})
    instance.client = client
    instance.save(update_fields=['client'])
    visits = client.visits_count()
    if visits >= 3:
        ManagerNotification.objects.create(
            message=f"Клиент {client} был у нас {visits} раз(а). Особое внимание при резервации {instance.id}",
            reservation=instance,
            level='warning' if visits < 6 else 'critical'
        )
        instance.flagged = True
        instance.save(update_fields=['flagged'])
