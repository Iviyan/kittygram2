from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Trip(models.Model):
    STATUS_CHOICES = (
        ('planned', 'Запланирована'),
        ('active', 'В пути'),
        ('completed', 'Завершена'),
    )

    cat = models.ForeignKey(
        'cats.Cat', on_delete=models.CASCADE, related_name='trips'
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='trips'
    )
    title = models.CharField(max_length=128)
    status = models.CharField(
        max_length=16, choices=STATUS_CHOICES, default='planned'
    )
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} ({self.cat.name})'


class Stop(models.Model):
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name='stops'
    )
    location_name = models.CharField(max_length=256)
    arrival_date = models.DateField()
    departure_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(
                fields=['trip', 'order'],
                name='unique_stop_order_per_trip'
            )
        ]

    def __str__(self):
        return f'{self.order}. {self.location_name}'
