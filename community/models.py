from django.contrib.auth import get_user_model
from django.db import models
from pets.models import Pet

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True
    )

    pets = models.ManyToManyField(
        Pet,
        related_name='tags',
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


from accounts.models import CustomUser


class Comment(models.Model):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    text = models.TextField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.pet.name}"