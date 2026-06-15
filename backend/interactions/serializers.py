from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from catalog.models import Film
from .models import Watchlist, Watched, Review
from catalog.serializers import FilmSerializer


class WatchlistSerializer(serializers.ModelSerializer):
    film = FilmSerializer(read_only=True)
    film_id = serializers.PrimaryKeyRelatedField(
        queryset=Film.objects.all(),
        source="film",
        write_only=True,
    )

    class Meta:
        model = Watchlist
        fields = ["id", "film", "film_id", "added_at"]
        read_only_fields = ["user", "added_at"]

    def validate(self, attrs):
        user = self.context["request"].user
        film = attrs.get("film")

        if Watchlist.objects.filter(user=user, film=film).exists():
            raise ValidationError({"detail": "This film is already in your watchlist."})

        return attrs


class WatchedSerializer(serializers.ModelSerializer):
    film = FilmSerializer(read_only=True)
    film_id = serializers.PrimaryKeyRelatedField(
        queryset=Film.objects.all(),
        source="film",
        write_only=True,
    )

    class Meta:
        model = Watched
        fields = ["id", "film", "film_id", "added_at"]
        read_only_fields = ["user", "added_at"]

    def validate(self, attrs):
        user = self.context["request"].user
        film = attrs.get("film")

        if Watched.objects.filter(user=user, film=film).exists():
            raise ValidationError(
                {"detail": "This film is already in your watched list."}
            )

        return attrs


class ReviewSerializer(serializers.ModelSerializer):
    film_id = serializers.PrimaryKeyRelatedField(
        queryset=Film.objects.all(),
        source="film",
    )

    class Meta:
        model = Review
        fields = ["id", "stars", "comment", "film_id", "added_at"]
        read_only_fields = ["id", "added_at"]

    def validate(self, attrs):
        if not self.instance:
            user = self.context["request"].user
            film = attrs.get("film")

            if not Watched.objects.filter(user=user, film=film).exists():
                raise ValidationError(
                    {"detail": "You cannot review a film that you haven't watched yet."}
                )

        return attrs
