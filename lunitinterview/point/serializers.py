from point.models import *
from rest_framework import serializers


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = '__all__'


class ContourPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContourPoint
        fields = (
            'longitude',
            'latitude',
        )


class ContourPointCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContourPoint
        fields = (
            'longitude',
            'latitude',
            'order'
        )


class ContourSerializer(serializers.ModelSerializer):
    coordinates = ContourPointSerializer(many=True, read_only=True)

    class Meta:
        model = Contour
        fields = (
            'id',
            'coordinates',
        )
