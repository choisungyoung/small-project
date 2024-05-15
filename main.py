import coordinate
import file
import process_image

directory_path = r"C:\\Users\\user\\Desktop\\me\\document\\회사\\sp\\aihub\\validation\\TS_AP25_1024\\304.토지피복지도_항공위성_이미지_원천\\01-1.정식개방데이터\\Validation\\01.원천데이터\\VS_AP25_1024픽셀.zip"
labeling_json_path = r"C:\\Users\\user\\Desktop\\me\\document\\회사\\sp\\aihub\\validation\\TS_AP25_1024\\304.토지피복지도_항공위성_이미지_라벨링_JSON\\01-1.정식개방데이터\\Validation\\02.라벨링데이터\\VL_AP25_1024픽셀_AP25_1024픽셀_Json.zip"
labeling_meta_path = r"C:\\Users\\user\\Desktop\\me\\document\\회사\\sp\\aihub\\validation\\TS_AP25_1024\\304.토지피복지도_항공위성_이미지_라벨링_Meta\\01-1.정식개방데이터\\Validation\\02.라벨링데이터\\VL_AP25_1024픽셀_AP25_1024픽셀_Meta.zip"

output_path = "output"
fileNameList = file.list_files_in_directory(directory_path=directory_path)

for fileName in fileNameList:

    origin_file_path = directory_path + "\\" + fileName + ".tif"
    output_file_path = output_path + "\\" + fileName + "_labeling.tif"
    json = file.read_json_file(labeling_json_path + "\\" + fileName + ".json")
    meta = file.read_json_file(labeling_meta_path + "\\" + fileName + "_META.json")

    left_top_coordinate = meta[0]["coordinates"].split(', ')
    
    left_top_coordinate_lat = float(left_top_coordinate[0])
    left_top_coordinate_lon = float(left_top_coordinate[1])

    print("left_top_coordinate : " + str(left_top_coordinate_lat) + " " + str(left_top_coordinate_lon))

    polygon_list = []
    for feature in json["features"]:
        ANN_NM = feature["properties"]["ANN_NM"]
        print(ANN_NM)

        pixel_list = []
        for coordinateValue in feature["geometry"]["coordinates"][0]:
            coordinate_pixel = coordinate.convert_to_pixel(left_top_coordinate_lat, left_top_coordinate_lon, coordinateValue[0], coordinateValue[1], 25)
            print("pixel : " + str(coordinate_pixel))
            pixel_list.append(coordinate_pixel)
        polygon_list.append(pixel_list)
        # break
    
    process_image.draw_lines_on_image(origin_file_path, polygon_list, output_file_path)
    break