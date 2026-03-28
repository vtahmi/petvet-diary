from django.db import models
from accounts.models import CustomUser
from datetime import date


class Pet(models.Model):
    SPECIES_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('other', 'Other'),
    ]

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='pets',
    )

    name = models.CharField(max_length=100)

    species = models.CharField(
        max_length=20,
        choices=SPECIES_CHOICES,
        default='dog'
    )

    date_of_birth = models.DateField()

    photo = models.ImageField(
        upload_to='pet_photos/',
        blank=True,
        null=True,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.owner.username})"

    @property
    def age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year
        if today.month < self.date_of_birth.month:
            age -= 1
        return age


class Vaccination(models.Model):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='vaccinations'
    )

    vaccine_name = models.CharField(max_length=200)

    date_given = models.DateField()

    next_due_date = models.DateField(
        blank=True,
        null=True,
    )

    veterinarian = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'user_type': 'vet'},
        related_name='vaccinations_given'
    )

    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_given']

    def __str__(self):
        return f"{self.vaccine_name} - {self.pet.name}"


class HealthCondition(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True
    )

    description = models.TextField(blank=True, null=True)

    pets = models.ManyToManyField(
        Pet,
        related_name='health_conditions',
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']