import coordinate
import file
import process_image

base_directory_path = r"data\304.토지피복지도_항공위성_이미지\01-1.정식개방데이터\Validation\\"
origin_path = base_directory_path + r"\01.원천데이터\VS_AP25_1024픽셀\\"
labeling_json_path = base_directory_path + r"\02.라벨링데이터\VL_AP25_1024픽셀_AP25_1024픽셀_Json\\"
labeling_meta_path = base_directory_path + r"\02.라벨링데이터\VL_AP25_1024픽셀_AP25_1024픽셀_Meta\\"

output_path = "output\\"
filename_list = file.list_files_in_directory(origin_path)

total = len(filename_list)
success_count = 0
fail_count = 0

for filename in filename_list:
    try:    
        origin_file_path = origin_path + filename + ".tif"
        output_file_path = output_path + filename + "_labeling.tif"
        json = file.read_json_file(labeling_json_path + filename + ".json")
        meta = file.read_json_file(labeling_meta_path + filename + "_META.json")

        left_top_coordinate = meta[0]["coordinates"].split(', ')
        img_resolution = meta[0]["img_resolution"]
        
        left_top_coordinate_lat = float(left_top_coordinate[0])
        left_top_coordinate_lon = float(left_top_coordinate[1])

        polygon_list = []
        for feature in json["features"]:
            ANN_NM = feature["properties"]["ANN_NM"]

            pixel_list = []
            for coordinateValue in feature["geometry"]["coordinates"][0]:
                coordinate_pixel = coordinate.convert_to_pixel(left_top_coordinate_lat, left_top_coordinate_lon, coordinateValue[0], coordinateValue[1], img_resolution)    # 해상도 25cm. 메타의 img_resolution : 0.25 
                pixel_list.append(coordinate_pixel)
            polygon_list.append(pixel_list)
        
        process_image.draw_lines_on_image(origin_file_path, polygon_list, output_file_path)

        success_count += 1
    except Exception as e:
        print(f"error : {e}")
        fail_count += 1

    # break

print(f"complete (total: {total}, success: {success_count}, fail:{fail_count})")