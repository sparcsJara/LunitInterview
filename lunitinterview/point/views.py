from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets

from point.backends import convert_point_to_GEOJson, convert_contour_to_GEOJson, extract_data_from_GEOJson
from point.serializers import *
from rest_framework import status

class PointViewSet(viewsets.ModelViewSet):
    queryset = Point.objects.all()
    serializer_class = PointSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response(convert_point_to_GEOJson(serializer.data,many=True))
        serializer = self.get_serializer(queryset, many=True)
        return Response(convert_point_to_GEOJson(serializer.data))

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(convert_point_to_GEOJson(serializer.data))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=extract_data_from_GEOJson(request.data))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = convert_point_to_GEOJson(serializer.data)
        data["id"] = serializer.data["id"]
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=extract_data_from_GEOJson(request.data), partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

class ContourViewSet(viewsets.ModelViewSet):
    queryset = Contour.objects.all()
    serializer_class = ContourSerializer
    contour_point_serializer = ContourPointCreateSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response(convert_contour_to_GEOJson(serializer.data,many=True))
        serializer = self.get_serializer(queryset, many=True)
        return Response(convert_contour_to_GEOJson(serializer.data))

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        return Response(convert_contour_to_GEOJson(serializer.data))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=extract_data_from_GEOJson(request.data))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = convert_contour_to_GEOJson(serializer.data)
        data["id"] = serializer.data["id"]
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        coordinates = serializer.initial_data["coordinates"]
        contour = serializer.save()
        order = 1
        for coordinate in coordinates:
            contour_point = {}
            contour_point["longitude"] = coordinate[0]
            contour_point["latitude"] = coordinate[1]
            contour_point["order"] = order
            contour_point_serializer = self.contour_point_serializer(data=contour_point)
            contour_point_serializer.is_valid(raise_exception=True)
            contour_point_serializer.save(contour=contour)
            order = order + 1

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=extract_data_from_GEOJson(request.data), partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        contour = serializer.instance
        ContourPoint.objects.filter(contour=contour).delete()
        coordinates = serializer.initial_data["coordinates"]
        order = 1
        for coordinate in coordinates:
            contour_point = {}
            contour_point["longitude"] = coordinate[0]
            contour_point["latitude"] = coordinate[1]
            contour_point["order"] = order
            contour_point_serializer = self.contour_point_serializer(data=contour_point)
            contour_point_serializer.is_valid(raise_exception=True)
            contour_point_serializer.save(contour=contour)
            order = order + 1