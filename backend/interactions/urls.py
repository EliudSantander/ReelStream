from rest_framework.routers import SimpleRouter

from .views import WatchlistViewSet, WatchedViewSet, ReviewViewSet

router = SimpleRouter()
router.register(r"watchlist", WatchlistViewSet, basename="watchlist")
router.register(r"watched", WatchedViewSet, basename="watched")
router.register(r"reviews", ReviewViewSet, basename="reviews")

urlpatterns = router.urls
