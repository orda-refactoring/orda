import requests
from utils.helpers import parse_data

def get_weather(lat, lon, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=en"
    
    response = requests.get(url)
    return response.json()

def get_direction(deg):
    if '22.5' <= deg < '67.5':
        return '북동'
    elif '67.5' <= deg < '112.5':
        return '동'
    elif '112.5' <= deg < '157.5':
        return '남동'
    elif '157.5' <= deg < '202.5':
        return '남'
        return '남서'
    elif '247.5' <= deg < '292.5':
        return '서'
    elif '292.5' <= deg < '337.5':
        return '북서'
    else:
        return '북'
    
def process_air_data(air_data):
    location_mapping = {
        '서울특별시': '서울',
        '제주도': '제주',
        '전라남도': '전남',
        '전라북도': '전북',
        '광주광역시': '광주',
        '경상남도': '경남',
        '경상북도': '경북',
        '울산광역시': '울산',
        '대구광역시': '대구',
        '부산광역시': '부산',
        '충청남도': '충남',
        '충청북도': '충북',
        '세종특별자치시': '세종',
        '대전광역시': '대전',
        '강원도': '영동',
        '경기도': '경기남부',
        '인천광역시': '인천'
    }

    fine_dust = parse_data(air_data['미세먼지'])
    ozone = parse_data(air_data['오존'])

    for key, value in location_mapping.items():
        fine_dust[key] = fine_dust.pop(value, 0)
        ozone[key] = ozone.pop(value, 0)

    return fine_dust, ozone    