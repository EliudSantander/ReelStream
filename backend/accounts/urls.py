from rest_framework.routers import SimpleRouter

from .views import UserViewset


router = SimpleRouter()
router.register(r"users", UserViewset, basename="users")

urlpatterns = router.urls
