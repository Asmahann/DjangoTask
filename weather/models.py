from django.db import models
from django.conf import settings

class PredictionQuery(models.Model):
    """
    Tracks prediction requests made by registered users, including coordinates, 
    requested dates, and the resulting precipitation prediction details.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='predictions'
    )
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    rain_sum = models.FloatField(default=0.0)
    precipitation_probability = models.FloatField(default=0.0)
    is_rainy = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Prediction Queries'

    def __str__(self):
        return f"{self.user.username} - {self.location} ({self.start_date} to {self.end_date})"
