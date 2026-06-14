from rest_framework.routers import SimpleRouter

from .views import WatchlistViewSet, WatchedViewSet

router = SimpleRouter()
router.register(r"watchlist", WatchlistViewSet, basename="watchlist")
router.register(r"watched", WatchedViewSet, basename="watched")

urlpatterns = router.urls
