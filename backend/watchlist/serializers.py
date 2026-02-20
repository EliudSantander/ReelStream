from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Watchlist
from catalog.serializers import FilmSerializer


class WatchlistSerializer(serializers.ModelSerializer):
    film = FilmSerializer(read_only=True)
    film_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Watchlist
        fields = "__all__"

    def create(self, validated_data):
        film_id = validated_data.pop("film_id")
        return Watchlist.objects.create(film_id=film_id, **validated_data)

    def validate(self, attrs):
        user = self.context["request"].user
        film_id = attrs.get("film_id")

        if Watchlist.objects.filter(user=user, film_id=film_id).exists():
            raise ValidationError({"detail": "This film is already in your watchlist."})

        return attrs
