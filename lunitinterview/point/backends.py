from point.GEOJson_type import GEOJSsonType
def convert_to_GEOJson(serializer_data, many=False):
    if many is False:
        data = convert_point_to_GEOJson(serializer_data)
        return data
    point_data_list = []
    for point_data in serializer_data:
        point_data_list.append(convert_to_GEOJson(point_data))
    data = {}
    data["Points"] = point_data_list
    return data

def convert_point_to_GEOJson(serializer_data):
    data = {}
    GEOJson_data = {}
    coordinate = [serializer_data["longitude"], serializer_data["latitude"]]
    GEOJson_data["type"] = GEOJSsonType.point.value
    GEOJson_data["coordinates"] = coordinate
    data["id"] = serializer_data["id"]
    data["data"] = GEOJson_data
    return data


def extract_data_from_GEOJson(data):
    if data["data"]["type"] == GEOJSsonType.point.value:
        point_data = {}
        point_data["longitude"] = data["data"]["coordinates"][0]
        point_data["latitude"] = data["data"]["coordinates"][1]
        return point_data
