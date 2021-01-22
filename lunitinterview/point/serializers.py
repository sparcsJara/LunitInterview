from point.models import *
from rest_framework import serializers


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = '__all__'


class ContourPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContourPoint
        fields = '__all__'


class ContourSerializer(serializers.ModelSerializer):
    coordinates = ContourPointSerializer(many=True, read_only=True)

    class Meta:
        model = Contour
        fields = (
            'id',
            'stories'
        )
        # auto_now_add나 auto_now가 true이면 read_only_fields여야 함.