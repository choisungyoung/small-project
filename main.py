import coordinate
import file
import process_image
import sys

base_directory_path = r"data\토지 피복지도 항공위성 이미지(수도권)\Training\\"

origin_path = base_directory_path + r"[원천]1.항공사진_Fine_512픽셀\\"
labeling_json_path = base_directory_path + r"[라벨]항공_512_2.Ground_Truth_JSON_전체\\"
labeling_meta_path = base_directory_path + r"[라벨]항공_512_4.메타데이터\\"

output_path = "output\\"

yolo_labeling_file_path = r"data\yolo\train\labels\\"
yolo_origin_file_path = r"data\yolo\train\images\\"
filename_list = file.list_files_in_directory(origin_path)

map = {"10":"0","20":"1","30":"2","40":"3","50":"4","60":"5","70":"6","80":"7","90":"8","100":"9"}

total = len(filename_list)
success_count = 0
fail_count = 0

for filename in filename_list:
    try:    
        origin_file_path_name = origin_path + filename + ".tif"
        output_file_path_name = output_path + filename + "_labeling.tif"
        json = file.read_json_file(labeling_json_path + filename + "_FGT.json", "utf-8")
        meta = file.read_json_file(labeling_meta_path + filename + "_META.json", "euc-kr")

        yolo_labeling_file_path_name = yolo_labeling_file_path + filename + ".txt"
        yolo_origin_file_path_name = yolo_origin_file_path + filename + ".tif"

        left_top_coordinate = meta[0]["coordinates"].split(', ')
        img_resolution = meta[0]["img_resolution"]
        
        left_top_coordinate_lat = float(left_top_coordinate[0])
        left_top_coordinate_lon = float(left_top_coordinate[1])

        polygon_list = []
        yolo_label = ""
        for feature in json["features"]:
            ANN_NM = feature["properties"]["ANN_NM"]
            ANN_CD = feature["properties"]["ANN_CD"]
            
            if ANN_CD != 10 and ANN_CD != 20:
                continue

            pixel_list = []
            min_width = sys.maxsize
            max_width = 0
            min_height = sys.maxsize
            max_height = 0
            for coordinateValue in feature["geometry"]["coordinates"][0]:
                coordinate_pixel = coordinate.convert_to_pixel(left_top_coordinate_lat, left_top_coordinate_lon, coordinateValue[0], coordinateValue[1], img_resolution)    # 해상도 25cm. 메타의 img_resolution : 0.25 
                min_width = min(min_width, coordinate_pixel[0])
                max_width = max(max_width, coordinate_pixel[0])
                min_height = min(min_height, coordinate_pixel[1])
                max_height = max(max_height, coordinate_pixel[1])

            pixel_list.append((min_width,min_height))
            pixel_list.append((min_width,max_height))
            pixel_list.append((max_width,max_height))
            pixel_list.append((max_width,min_height))
            pixel_list.append((min_width,min_height))
            polygon_list.append(pixel_list)

            # labeling 데이터 생성

            center_x = (min_width + max_width) / 2
            center_y = (min_height + max_height) / 2
            object_width = max_width - min_width
            object_height = max_height - min_height

            # 중심 표시
            polygon_list.append([(center_x, center_y), (center_x, center_y + 1), (center_x + 1, center_y + 1), (center_x + 1, center_y), (center_x, center_y)])

            image_size = process_image.get_image_width_height(origin_file_path_name)

            center_x_ratio = center_x / image_size[0]
            center_y_ratio = center_y / image_size[1]
            object_width_ratio = object_width / image_size[0]
            object_height_ratio = object_height / image_size[1]
            yolo_label +=  map[str(ANN_CD)] + " " + str(center_x_ratio) + " " + str(center_y_ratio) + " " + str(object_width_ratio) + " " + str(object_height_ratio) + "\n"
            
            # print(">>> " + yolo_label)

            # break

        # 라벨링 데이터 저장 (yolo)
        print(yolo_label)
        file.save_list_file(yolo_labeling_file_path_name, yolo_label)

        # 원천 이미지 yolo 디렉토리로 복사
        file.copy_file(origin_file_path_name, yolo_origin_file_path_name)

        process_image.draw_lines_on_image(origin_file_path_name, polygon_list, output_file_path_name)

        success_count += 1

        if success_count > 100:
            break
    except Exception as e:
        print(f"error : {e}")
        fail_count += 1

    # break

print(f"complete (total: {total}, success: {success_count}, fail:{fail_count})")