from django.contrib import admin
from django.urls import path, include, re_path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.http import JsonResponse


def custom_404_view(request, exception=None):
    return JsonResponse(
        {"error": "This resource does not exists", "status_code": 404}, status=404
    )


handler404 = custom_404_view


urlpatterns = [
    # YOUR PATTERNS
    path("admin/", admin.site.urls),
    path("api/v1/", include("catalog.urls")),
    path("api/v1/", include("watchlist.urls")),
    path("api/v1/", include("accounts.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # UI:
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    re_path(r"^.*$", handler404),
]
