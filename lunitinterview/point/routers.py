from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter

from lunitinterview.point.views import PointViewSet, ContourViewSet

PointRouter = SimpleRouter()

PointRouter.register(
    prefix=r'points',
    viewset=PointViewSet,
)

PointRouter.register(
    prefix=r'contours',
    viewset=ContourViewSet,
)
