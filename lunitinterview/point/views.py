from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from point.models import *
from point.serializers import *
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action


# Create your views here.

class PointViewSet(viewsets.ModelViewSet):
    queryset = Point.objects.all()
    serializer_class = PointSerializer


class ContourViewSet(viewsets.ModelViewSet):
    queryset = Contour.objects.all()
    serializer_class = ContourSerializer
