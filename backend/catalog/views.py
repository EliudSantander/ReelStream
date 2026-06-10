from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from drf_spectacular.utils import extend_schema

from .models import Film
from .serializers import FilmSerializer
from .filters import FilmFilter

# @extend_schema(tags=["Films"])
# class FilmViewSet(ReadOnlyModelViewSet):
#     queryset = Film.objects.all()
#     serializer_class = FilmSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [FilmFilter]


@extend_schema(tags=["Films"])
class FilmViewSet(ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    filter_backends = [FilmFilter]

    def get_permissions(self):
        """
        Allows writing methods only to Admin Users
        """
        permission_classes = []
        if self.action not in ["list", "retrieve"]:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
