from PIL import Image, ImageDraw

def draw_lines_on_image(image_path, polygons, output_path):
    # 이미지 열기
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # 다각형 그리기
    for polygon in polygons:
        if len(polygon) > 2:
            draw.polygon(polygon, outline='red', width=2)

    # 결과 이미지 저장
    image.save(output_path)
    print(f"success save image: {output_path}")

def get_image_width_height(image_path):
    image = Image.open(image_path)
    return (image.width, image.height)
