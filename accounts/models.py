from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('owner', 'Pet Owner'),
        ('vet', 'Veterinarian'),
    ]

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='owner',
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
    )

    bio = models.TextField(
        max_length=500,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    @property
    def is_owner(self):
        return self.user_type == 'owner'

    @property
    def is_vet(self):
        return self.user_type == 'vet'


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    address = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    clinic_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"