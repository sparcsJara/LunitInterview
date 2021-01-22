from django.db import models

class Coordinate(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()

    class Meta:
        abstract = True

class Point(Coordinate):
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(longitude__gte=-180), name='longitude_gte_minus_180'),
            models.CheckConstraint(check=models.Q(longitude__lte=180), name='longitude_lte_180'),
            models.CheckConstraint(check=models.Q(latitude__gte=-90), name='latitude_gte_minus_90'),
            models.CheckConstraint(check=models.Q(latitude__lte=90), name='latitude_lte_90'),
        ]

class Contour(models.Model):
    pass

class ContourPoint(Coordinate):
    contour = models.ForeignKey(
        Contour,
        related_name='coordinate',
        on_delete=models.CASCADE
    )
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(longitude__gte=-180), name='cp_longitude_gte_minus_180'),
            models.CheckConstraint(check=models.Q(longitude__lte=180), name='cp_longitude_lte_180'),
            models.CheckConstraint(check=models.Q(latitude__gte=-90), name='cp_latitude_gte_minus_90'),
            models.CheckConstraint(check=models.Q(latitude__lte=90), name='cp_latitude_lte_90'),
        ]



