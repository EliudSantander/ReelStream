from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from .models import Film
from .serializers import FilmSerializer
from .filters import FilmFilter


@extend_schema(tags=["Films"])
class FilmViewSet(ReadOnlyModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [FilmFilter]
