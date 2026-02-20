from django.db import models
from django.conf import settings


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
