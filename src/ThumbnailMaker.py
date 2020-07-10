import os

# pip install svglin
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

# pip
from PIL import Image, ImageDraw, ImageFont


def make_thumbnail(path, thumbnail_text, color):
    thumbnail_template_url = "assets\\images\\thumbnail_template.svg"
    theme_color = color.lstrip("#").lower()
    color = (int(theme_color[0:2], 16), int(
        theme_color[2:4], 16), int(theme_color[4:6], 16))

    template_svg_file = open(thumbnail_template_url, "r", encoding='UTF8')
    new_template_svg = open(
        "assets\\files\\thumbnail_template.svg", "w", encoding='UTF8')
    template_svg_content = template_svg_file.read()
    template_svg_change_color = template_svg_content.replace(
        "red", "#" + theme_color)
    new_template_svg.write(template_svg_change_color)
    template_svg_file.close()
    new_template_svg.close()

    drawing = svg2rlg("assets\\files\\thumbnail_template.svg")
    renderPM.drawToFile(drawing, "assets\\files\\template.png", fmt="PNG")

    image = Image.open('assets\\files\\template.png')
    font_type_GodoB = ImageFont.truetype('assets\\fonts\\godo\\GodoB.ttf', 60)
    font_type_GodoM = ImageFont.truetype('assets\\fonts\\godo\\GodoM.ttf', 60)
    font_type_godoRounded_L = ImageFont.truetype(
        'assets\\fonts\\godo\\godoRounded L.ttf', 128)

    num_X_position = image.size[0] - \
        font_type_godoRounded_L.getsize(thumbnail_text[0])[0] - 20
    num_Y_position = -12  # 픽셀 세어본거. 폰트 바뀌면 그거에 맞춰서 바꿔줘야 함.

    text_Y_position = [
        (image.size[1] / 2) -
        (font_type_GodoM.getsize(thumbnail_text[1])[1] / 2) - 90,
        (image.size[1] / 2) -
        (font_type_GodoB.getsize(thumbnail_text[2])[1] / 2),
        (image.size[1] / 2) -
        (font_type_GodoM.getsize(thumbnail_text[3])[1] / 2) + 90
    ]

    draw = ImageDraw.Draw(image)
    draw.text(xy=(num_X_position, num_Y_position), text=thumbnail_text[0], fill=(
        255, 255, 255), font=font_type_godoRounded_L)
    draw.text(xy=(20, text_Y_position[0]), text=thumbnail_text[1], fill=(
        255, 255, 255), font=font_type_GodoM)
    if theme_color == "ffffff":
        draw.text(xy=(20, text_Y_position[1]), text=thumbnail_text[2], fill=(
            255, 255, 255), font=font_type_GodoB)
    else:
        draw.text(xy=(
            20, text_Y_position[1]), text=thumbnail_text[2], fill=color, font=font_type_GodoM)
    draw.text(xy=(20, text_Y_position[2]), text=thumbnail_text[3], fill=(
        255, 255, 255), font=font_type_GodoM)
    image.show()
    image.save(path.rstrip("/") + "/thumbnail.png", "PNG")


make_thumbnail("C:/Users/seong/OneDrive/Documents/Personal/학교",
               ["12", "우와", "쩐다", "대박"], "#ffffff")
