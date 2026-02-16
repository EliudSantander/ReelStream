from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Film
from .serializers import FilmSerializer


class FilmViewSet(ReadOnlyModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
