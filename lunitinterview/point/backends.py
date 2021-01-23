from rest_framework.exceptions import ValidationError
from shapely.geometry import Polygon
from point.GEOJson_type import GEOJSsonType
from point.models import Contour, Point, ContourPoint


def convert_point_to_GEOJson(serializer_data, many=False):
    if many is False:
        data = convert_single_point_to_GEOJson(serializer_data)
        return data
    point_data_list = []
    for point_data in serializer_data:
        point_data_list.append(convert_single_point_to_GEOJson(point_data))
    data = {}
    data["points"] = point_data_list
    return data

def convert_single_point_to_GEOJson(serializer_data):
    data = {}
    GEOJson_data = {}
    coordinate = [serializer_data["longitude"], serializer_data["latitude"]]
    GEOJson_data["type"] = GEOJSsonType.point.value
    GEOJson_data["coordinates"] = coordinate
    data["id"] = serializer_data["id"]
    data["data"] = GEOJson_data
    return data


def convert_contour_to_GEOJson(serializer_data, many=False):
    if many is False:
        data = convert_single_contour_to_GEOJson(serializer_data)
        return data
    return_list = []
    for contour_data in serializer_data:
        return_list.append(convert_single_contour_to_GEOJson(contour_data))
    data = {}
    data["contours"] = return_list
    return data

def convert_single_contour_to_GEOJson(serializer_data):
    data = {}
    GEOJson_data = {}
    coordinates = []
    for contour_point in serializer_data["coordinates"]:
        coordinate = [contour_point["longitude"], contour_point["latitude"]]
        coordinates.append(coordinate)
    GEOJson_data["type"] = GEOJSsonType.contour.value
    GEOJson_data["coordinates"] = coordinates
    data["id"] = serializer_data["id"]
    data["data"] = GEOJson_data
    return data

def extract_data_from_GEOJson(data):
    if data["data"]["type"] == GEOJSsonType.point.value:
        point_data = {}
        point_data["longitude"] = data["data"]["coordinates"][0]
        point_data["latitude"] = data["data"]["coordinates"][1]
        return point_data
    elif data["data"]["type"] == GEOJSsonType.contour.value:
        contour_data = {}
        contour_data["coordinates"] = data["data"]["coordinates"]
        return contour_data

def check_whether_is_inside(point, contour):
    assert isinstance(point, Point) or isinstance(point, ContourPoint)
    assert isinstance(contour, Contour)
    crosses = 0
    contour_points = contour.coordinates.all()
    for i in range(0,len(contour_points)):

        j = (i+1) % len(contour_points)
        contour_point = contour_points[i]
        next_point = contour_points[j]
        # point가 선분 [contour_point와 next_point를 잇는 선분]의 latitude 범위 사이에 있음
        if (contour_point.latitude > point.latitude) != (next_point.latitude > point.latitude):
            # cross longitude는 point를 지나는 수평선과 선분의 교점
            cross_longitude = ((point.latitude-next_point.latitude)*contour_point.longitude-(point.latitude-contour_point.latitude)*next_point.longitude)/(contour_point.latitude-next_point.latitude)
            # cross longitude 가 오른쪽 반직선과의 교점이 맞으면 교점의 개수를 증가시킴
            if (point.longitude < cross_longitude):
                crosses = crosses + 1
    return (crosses % 2) == 1

def calculate_intersection_area(contour1, contour2):
    assert isinstance(contour1, Contour)
    assert isinstance(contour2, Contour)

    is_inside = False
    # step 0: check whether there is a intersection between them
    contour_points1 = contour1.coordinates.all()
    contour_points2 = contour2.coordinates.all()
    for contour_point in contour_points2:
        if check_whether_is_inside(contour_point, contour1):
            is_inside = True
            break
    if not is_inside:
        raise ValidationError("There is no interaction between the contours.")

    # step 1 caluclate intersection area through shapely
    contour1_coordinates = []
    for contour_point in contour_points1:
        contour1_coordinates.append([contour_point.longitude,contour_point.latitude])
    contour2_coordinates = []
    for contour_point in contour_points2:
        contour2_coordinates.append([contour_point.longitude, contour_point.latitude])
    contour1_polygon = Polygon(contour1_coordinates)
    contour2_polygon = Polygon(contour2_coordinates)

    return contour1_polygon.intersection(contour2_polygon).area
