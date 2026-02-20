from django.contrib.auth.models import User
from rest_framework import mixins, viewsets, permissions
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from .serializers import UserSerializer
from .permissions import IsSelf


@extend_schema(tags=["Users"])
class UserViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        if self.action == "me":
            return [permissions.IsAuthenticated()]
        return [IsSelf()]

    @action(detail=False, methods=["get", "patch", "put"])
    def me(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if request.method in ["PATCH", "PUT"]:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)
