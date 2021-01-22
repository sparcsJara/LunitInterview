from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets

from point.backends import convert_to_GEOJson, extract_data_from_GEOJson
from point.models import *
from point.serializers import *
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

class PointViewSet(viewsets.ModelViewSet):
    queryset = Point.objects.all()
    serializer_class = PointSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response(convert_to_GEOJson(serializer.data,many=True))
        serializer = self.get_serializer(queryset, many=True)
        return Response(convert_to_GEOJson(serializer.data))

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(convert_to_GEOJson(serializer.data))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=extract_data_from_GEOJson(request.data))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = convert_to_GEOJson(serializer.data)
        data["id"] = serializer.data["id"]
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

class ContourViewSet(viewsets.ModelViewSet):
    queryset = Contour.objects.all()
    serializer_class = ContourSerializer
