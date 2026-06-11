from rest_framework.routers import SimpleRouter

from .views import WatchlistViewSet


router = SimpleRouter()
router.register(r"watchlist", WatchlistViewSet, basename="watchlist")

urlpatterns = router.urls
