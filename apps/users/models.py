from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    # username, password уже есть
    role = models.CharField(
        max_length=20,
        choices=[
            ('admin', 'Админ'),
            ('manager', 'Менеджер'),
        ]
    )
