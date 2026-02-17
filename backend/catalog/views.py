from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Film
from .serializers import FilmSerializer


class FilmViewSet(ReadOnlyModelViewSet):
    serializer_class = FilmSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        queryset = Film.objects.all().order_by("film_id")
        title = self.request.query_params.get("title")
        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset
