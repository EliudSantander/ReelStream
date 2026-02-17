from rest_framework.routers import SimpleRouter

from .views import FilmViewSet


router = SimpleRouter()
router.register(r"films", FilmViewSet, basename="film")

urlpatterns = router.urls
