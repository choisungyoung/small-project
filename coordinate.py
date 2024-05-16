from math import sqrt

def convert_to_pixel(base_lat, base_lon, lat, lon, resolution):
    # 입력 EPSG:5186 좌표계
    # base_lat, base_lon : 좌측 상단 좌표값
    # lat, lon : 픽셀좌표로 변환할 좌표값
    # resolution :  해상도

    x = lat - base_lat
    y = base_lon - lon

    return (x / resolution, y / resolution)