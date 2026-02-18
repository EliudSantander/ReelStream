from django.db import models


class Film(models.Model):

    class Rating(models.TextChoices):
        G = "G", "General Audiences"
        PG = "PG", "Parental Guidance Suggested"
        PG_13 = "PG-13", "Parents Strongly Cautioned"
        R = "R", "Restricted"
        NC_17 = "NC-17", "Adults Only"

    film_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    release_year = models.IntegerField(blank=True, null=True)
    rating = models.CharField(
        max_length=6,
        choices=Rating.choices,
        default=Rating.G,
    )

    class Meta:
        db_table = "film"
        managed = False
