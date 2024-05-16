import os
import json

def list_files_in_directory(directory_path):
    try:
        # 주어진 디렉토리의 파일 목록을 가져오기
        files = os.listdir(directory_path)
        
        # 확장자를 제거한 파일명 리스트 생성
        file_names = [os.path.splitext(file)[0] for file in files]
        
        return file_names
    except Exception as e:
        print(f"Error: {e}")

def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__=="__main__":
    # test
    base_directory_path = r"data\304.토지피복지도_항공위성_이미지\01-1.정식개방데이터\Validation\\"
    origin_path = base_directory_path + r"C\01.원천데이터\VS_AP25_1024픽셀\\"
    labeling_json_path = base_directory_path + r"\02.라벨링데이터\VL_AP25_1024픽셀_AP25_1024픽셀_Json\\"
    labeling_meta_path = base_directory_path + r"\02.라벨링데이터\VL_AP25_1024픽셀_AP25_1024픽셀_Meta\\"

    # 함수 호출
    list_files_in_directory(origin_path)

    json = read_json_file(labeling_json_path + "\\" + "LC_GG_AP25_36701005_001_2021_1024.json")

    print(json["features"][0]["geometry"]["coordinates"])