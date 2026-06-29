from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    CITIZEN = "CITIZEN", "Citizen"
    OFFICER = "OFFICER", "Officer"
    DISPATCHER = "DISPATCHER", "Dispatcher"
    ADMIN = "ADMIN", "Admin"


class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CITIZEN
    )
    # Optional: Add fields like phone number, profile pic, etc.
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
