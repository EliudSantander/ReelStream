from django.contrib.auth.models import User
from rest_framework import mixins, status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .serializers import UserSerializer
from .permissions import IsSelf, IsNotAuthenticated


@extend_schema(tags=["Users"])
class UserViewset(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = None

    def get_permissions(self):
        permission_classes = []
        if self.action == "create":
            permission_classes = [IsNotAuthenticated]
        if self.action == "me":
            permission_classes = [permissions.IsAuthenticated, IsSelf]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["get", "patch", "delete"])
    def me(self, request):
        user = request.user

        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        elif request.method == "PATCH":
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        elif request.method == "DELETE":
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
