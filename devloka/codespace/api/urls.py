from codespace.api.api import CodeSpaceViewSet, SyntaxViewSet
from rest_framework.routers import DefaultRouter

app_name = "codespace"

router = DefaultRouter()

router.register(r"codespaces", CodeSpaceViewSet, basename="codespaces")
router.register(r"syntax", SyntaxViewSet, basename="syntax")

urlpatterns = router.urls
