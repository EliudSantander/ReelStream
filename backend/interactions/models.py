from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Watchlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="watchlist",
    )
    film = models.ForeignKey(
        "catalog.Film",
        on_delete=models.CASCADE,
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "film"]

    def __str__(self):
        return f"{self.user} - {self.film}"


class Watched(models.Model):
    film = models.ForeignKey(
        "catalog.Film",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="watched_films",
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "film"]

    def __str__(self):
        return f"{self.user} - {self.film}"


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    film = models.ForeignKey("catalog.Film", on_delete=models.CASCADE)
    stars = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, "Min value is 1 star."),
            MaxValueValidator(5, "Max value is 5 stars."),
        ],
    )
    comment = models.TextField(max_length=200, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["film", "user"]

    def __str__(self):
        comment = self.comment if self.comment else "No comment created"
        return f"{self.film} - {self.stars} stars - {comment}"
