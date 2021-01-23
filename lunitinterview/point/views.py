from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets

from point.backends import convert_point_to_GEOJson, convert_contour_to_GEOJson, extract_data_from_GEOJson, \
    check_whether_is_inside, calculate_intersection_area
from point.serializers import *
from rest_framework import status

class PointViewSet(viewsets.ModelViewSet):
    queryset = Point.objects.all()
    serializer_class = PointSerializer

    def inside_quersyet(self, contour_id):
        try:
            contour = Contour.objects.get(pk=int(contour_id))
        except Contour.DoesNotExist:
            raise ValidationError("The requested contour does not exist.")
        max_longitude = -180
        min_longitude = 180
        max_latitude = -90
        min_latitude = 90
        for contour_point in contour.coordinates.all():
            max_longitude = max(contour_point.longitude, max_longitude)
            min_longitude = min(contour_point.longitude, min_longitude)
            max_latitude = max(contour_point.latitude, max_latitude)
            min_latitude = min(contour_point.latitude, min_latitude)
        points = Point.objects.filter(longitude__gte=min_longitude, longitude__lte=max_longitude,
                                      latitude__gte=min_latitude, latitude__lte=max_latitude)
        queryset = []
        for point in points:
            if check_whether_is_inside(point, contour):
                queryset.append(point)
        return queryset

    def list(self, request, *args, **kwargs):
        contour_id = request.GET.get('contour', None)
        if contour_id:
            queryset = self.inside_quersyet(contour_id)
        else:
            queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return Response(convert_point_to_GEOJson(serializer.data, many=True))

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
        data = convert_contour_to_GEOJson(serializer.data)
        data["id"] = serializer.data["id"]
        return Response(data)

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

        data = convert_contour_to_GEOJson(serializer.data)
        data["id"] = serializer.data["id"]

        return Response(data)

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

    @action(detail=True, url_path='intersection', url_name='intersection')
    def intersection(self, request, pk=None):
        instance = self.get_object()
        contour1_id = pk
        contour2_id = request.GET.get('contour', None)
        if pk is None or contour2_id is None:
            raise ValidationError("Please input contour_id")
        try:
            contour1 = Contour.objects.get(pk=int(contour1_id))
        except Contour.DoesNotExist:
            raise ValidationError("The requested contour does not exist.")
        try:
            contour2 = Contour.objects.get(pk=int(contour2_id))
        except Contour.DoesNotExist:
            raise ValidationError("The requested contour does not exist.")
        intersection_area = calculate_intersection_area(contour1, contour2)
        contour_list =[contour1, contour2]
        serializer = self.get_serializer(contour_list, many=True)
        contour_list = convert_contour_to_GEOJson(serializer.data,many=True)["contours"]
        contour_list.append(intersection_area)
        response_dict = {"intersections": contour_list}
        return Response(response_dict)