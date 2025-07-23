from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    usable_password = models.BooleanField(default=True)
    national_id = models.CharField(max_length=10, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
