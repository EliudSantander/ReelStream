from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from .models import Watchlist, Watched
from .serializers import WatchlistSerializer, WatchedSerializer


@extend_schema(tags=["Watchlist"])
class WatchlistViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        film = serializer.validated_data["film"]

        try:
            with transaction.atomic():
                serializer.save(user=self.request.user)
                Watched.objects.filter(user=user, film=film).delete()
        except IntegrityError as e:
            raise ValidationError(
                {"detail": "The film was not correctly saved", "error": str(e)},
            )


@extend_schema(tags=["Watched"])
class WatchedViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = WatchedSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Watched.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        film = serializer.validated_data["film"]

        try:
            with transaction.atomic():
                serializer.save(user=user)
                Watchlist.objects.filter(user=user, film=film).delete()
        except IntegrityError as e:
            raise ValidationError(
                {"detail": "The film was not correctly saved", "error": str(e)},
            )
