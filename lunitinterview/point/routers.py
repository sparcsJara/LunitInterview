from rest_framework.routers import SimpleRouter

from point.views import PointViewSet, ContourViewSet

router = SimpleRouter()

router.register(
    prefix=r'points',
    viewset=PointViewSet,
)

router.register(
    prefix=r'contours',
    viewset=ContourViewSet,
)
