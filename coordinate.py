from pyproj import Proj, transform
from math import sqrt

def getDistance(x1, y1, x2, y2):
    # EPSG:5186 좌표계 정의
    proj_5186 = Proj(init='epsg:5186')

    # 두 지점의 좌표 (x, y)
    point1 = (x1, y1)
    point2 = (x2, y2)

    # 두 지점 사이의 거리 계산 (단위: 미터)
    distance = sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

    print(f"두 지점 사이의 거리: {distance} 미터")
    return distance

def convert_to_pixel(base_lat, base_lon, lat, lon, resolution):
    # 입력 EPSG:5186 좌표계
    # resolution (cm)

    x = lat - base_lat
    y = base_lon - lon

    return (x / (resolution / 100), y / (resolution / 100))

if __name__=="__main__":
    getDistance(209127.008540217822883, 487683.381334160629194, 209118.807840511435643, 487668.282318552723154)