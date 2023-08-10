import requests

def get_weather(lat, lon, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=en"
    
    response = requests.get(url)
    return response.json()

def parse_data(data_str):
    parsed_data = {}
    entries = data_str.split(',')
    for entry in entries:
        key, value = entry.split(':')
        parsed_data[key.strip()] = value.strip()
    return parsed_data

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