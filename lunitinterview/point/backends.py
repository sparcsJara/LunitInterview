from point.GEOJson_type import GEOJSsonType

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