from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema

from .permissions import IsOwnerOrReadOnly

from .models import Watchlist, Watched, Review
from .serializers import WatchlistSerializer, WatchedSerializer, ReviewSerializer


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


@extend_schema(tags=["Reviews"])
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Review.objects.all()

        film_id = self.request.query_params.get("film_id")
        if film_id is not None:
            queryset = queryset.filter(film_id=film_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
