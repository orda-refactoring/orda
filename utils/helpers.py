from django.contrib.gis.serializers.geojson import Serializer
from mountains.models import Course, CourseDetail

def parse_data(data_str):
    parsed_data = {}
    entries = data_str.split(',')
    for entry in entries:
        key, value = entry.split(':')
        parsed_data[key.strip()] = value.strip()
    return parsed_data

def serialize_courses(obj_list, *fields):
    serializer = Serializer()
    course_data = {}

    if isinstance(obj_list[0], Course):
        for obj in obj_list:
            geojson_data = serializer.serialize([obj], fields=fields)
            course_data[obj.pk] = geojson_data
    elif isinstance(obj_list[0], CourseDetail):
        geojson_data = serializer.serialize(obj_list, fields=fields)
        course_data[obj_list[0].crs_name_detail.pk] = geojson_data
    return course_data
