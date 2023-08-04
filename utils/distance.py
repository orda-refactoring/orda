from accounts.models import *

def mountain_distance(user, mountain):
    if user.is_authenticated:
        try:
            user_latitude = user.userlocation.latitude
            user_longitude = user.userlocation.longitude
        except UserLocation.DoesNotExist:
            user_latitude = None
            user_longitude = None
    else:
        user_latitude = None
        user_longitude = None

    mountain_distance = mountain.current_location(user_latitude, user_longitude)

    return mountain_distance


def mountains_distance(user, mountains):
    if user.is_authenticated:
        try:
            user_latitude = user.userlocation.latitude
            user_longitude = user.userlocation.longitude
        except UserLocation.DoesNotExist:
            user_latitude = None
            user_longitude = None
    else:
        user_latitude = None
        user_longitude = None

    mountain_distance_lst = []

    for mountain in mountains:
        mountain_distance = mountain.current_location(user_latitude, user_longitude)
        mountain_distance_lst.append(mountain_distance)

    return mountain_distance_lst