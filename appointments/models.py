from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from pets.models import Pet

User = get_user_model()

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='appointments_as_owner',
        limit_choices_to={'user_type': 'owner'}
    )

    veterinarian = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments_as_vet',
        limit_choices_to={'user_type': 'vet'}
    )

    appointment_date = models.DateTimeField()

    reason = models.CharField(max_length=200)

    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-appointment_date']

    def __str__(self):
        return f"{self.pet.name} - {self.appointment_date.strftime('%Y-%m-%d %H:%M')}"
