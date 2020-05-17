# pip install watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import time

import os
# pip install zipfile
import zipfile
# pip install clipboard
import clipboard

# pip
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

# pip
from PIL import Image, ImageDraw, ImageFont

import urllib


def make_output_date(MM, DD, YY, TT, A_P):
    if MM == 'Jan':
        MM = '1월 '
    elif MM == 'Feb':
        MM = '2월 '
    elif MM == 'Mar':
        MM = '3월 '
    elif MM == 'Apr':
        MM = '4월 '
    elif MM == 'May':
        MM = '5월 '
    elif MM == 'Jun':
        MM = '6월 '
    elif MM == 'Jul':
        MM = '7월 '
    elif MM == 'Aug':
        MM = '8월 '
    elif MM == 'Sep':
        MM = '9월 '
    elif MM == 'Oct':
        MM = '10월 '
    elif MM == 'Nov':
        MM = '11월 '
    elif MM == 'Dec':
        MM = '12월 '
    else:
        MM = '??월 '

    if A_P == 'AM':
        A_P = '오전 '
    elif A_P == 'PM':
        A_P = '오후 '
    else:
        A_P = ''

    T_hour, T_min = TT.split(':')

    date = YY + '년 ' + MM + DD.rstrip(',') + \
        '일 ' + A_P + T_hour + '시 ' + T_min + '분'
    return date


def search_page_title(file_content):
    # html 파일에서 <h1 class="page-title"> 태그 안에 있는 제목을 꺼내서 ".html"이라고 확장자명을 추가하여 new_name 에 저장
    title = file_content.split('<h1 class="page-title">')[1].split('</h1>')[0]
    # page_title 예외처리.. 제목에 소괄호()가 있으면 <mark> 태그가 붙어있음.
    # mark 태그를 제거
    title = title.replace("<mark class=\"highlight-gray\">",
                          "").replace("</mark>", "")
    file_name = title.split(' - ')[0]
    return title, file_name


def extract_thumbnail_title(html):
    title = html.split("</blockquote>")[0].split('class="">')[1]
    thumbnail_title = ["", "", "", ""]
    # 카테고리 내에서 게시물 번호
    thumbnail_title[0] = html.split("Number in Project</th><td>")[1]
    thumbnail_title[0] = thumbnail_title[0].split('</td>')[0]
    # 썸네일 첫번째 줄
    thumbnail_title[1] = title.split("<strong>")[0].strip(" -")
    # 썸네일 두번째 줄
    thumbnail_title[2] = title.split("<strong>")[1]
    thumbnail_title[2] = thumbnail_title[2].split("</strong>")[0].strip(" ")
    # 썸네일 세번째 줄
    thumbnail_title[3] = title.split("</strong>")[1].strip(" ")
    return thumbnail_title


def make_thumbnail(url, thumbnail_text, color):
    thumbnail_template_url = "assets\\images\\thumbnail_template.svg"
    theme_color = color.lstrip("#").lower()
    color = (int(theme_color[0:2], 16), int(
        theme_color[2:4], 16), int(theme_color[4:6], 16))

    template_svg_file = open(thumbnail_template_url, "r", encoding='UTF8')
    new_template_svg = open(
        "assets\\thumbnail_template.svg", "w", encoding='UTF8')
    template_svg_content = template_svg_file.read()
    template_svg_change_color = template_svg_content.replace(
        "red", "#" + theme_color)
    new_template_svg.write(template_svg_change_color)
    template_svg_file.close()
    new_template_svg.close()

    drawing = svg2rlg("assets\\thumbnail_template.svg")
    renderPM.drawToFile(drawing, "assets\\template.png", fmt="PNG")

    image = Image.open('assets\\template.png')
    font_type_GodoB = ImageFont.truetype('assets\\fonts\\godo\\GodoB.ttf', 60)
    font_type_GodoM = ImageFont.truetype('assets\\fonts\\godo\\GodoM.ttf', 60)
    font_type_godoRounded_L = ImageFont.truetype(
        'assets\\fonts\\godo\\godoRounded L.ttf', 128)

    num_X_position = image.size[0] - \
        font_type_godoRounded_L.getsize(thumbnail_text[0])[0] - 20
    num_Y_position = -12  # 픽셀 세어본거. 폰트 바뀌면 그거에 맞춰서 바꿔줘야 함. X처럼 안한 이유는 폰트가 ㅈ같아서

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
    # image.show()
    image.save(url + "thumbnail.png", "PNG")


def change_url(url):
    website = ""
    if url[:8] == 'https://':
        mark = url[8:].find('/')
        website = url[8:mark+8]
    elif url[:7] == 'http://':
        mark = url[7:].find('/')
        website = url[7:mark]
    else:
        mark = url.find('/')
        website = url[:mark]

    if website == 'www.youtube.com':
        url = url.replace('watch?v=', 'embed/')
    elif website == 'codepen.io':
        url = url.replace('/pen/', '/embed/') + \
            '?theme-id=dark&default-tab=html,result'
    elif website == 'whimsical.com':
        url = "https://whimsical.com/embed" + url[url.rfind('/'):]
    elif website == 'www.figma.com':
        url = 'https://www.figma.com/embed?embed_host=share&url=https' + \
            urllib.parse.quote("://") + website + \
            urllib.parse.quote(url[url.rfind('/file/'):])
    else:
        url = url

    return url


def make_embed(file_content):
    mark_1 = 0
    mark_2 = 1

    while True:
        if file_content[mark_1:].find('<div class="source"><a href="') == -1:
            break
        mark_1 = mark_1 + \
            file_content[mark_1:].find('<div class="source"><a href="') + 29
        mark_2 = mark_1 + file_content[mark_1:].find('">')
        mark_3 = mark_1 + file_content[mark_1:].find('</a></div></figure>')
        url = file_content[mark_1:mark_2]
        url = change_url(url)
        file_content = file_content[:(mark_1-29)] + '<div class="embed_container"><a href="' + \
            url + '"><iframe src="' + url + \
            '" class="embed_inner"></iframe>' + file_content[mark_3:]

    return file_content


def change_content(file_content):
    # 티스토리에서 인식 가능하게 article 태그 이외 앞뒤 태그들 삭제 및 클래스 추가
    changed_content = file_content.split('<body>')[1].split(
        '</body>')[0].replace('page sans\">', 'Notion_P page sans\">')
    # html 파일에서 properties 표 안에 있는 페이지 생성 날자를 빼내서 저장. (밑에서 add_content에 추가)
    created_date = changed_content.split(
        'Created Time</th><td><time>@')[1].split('</time></td></tr>')[0]
    created_Month, created_Day, created_Year, created_Time, is_AM = created_date.split(
        ' ')
    created_date = make_output_date(
        created_Month, created_Day, created_Year, created_Time, is_AM)

    # 내용이 비어있는 <p> 태그도 제대로 비어있는 한줄이 출력되게끔 끝에 공백 추가
    changed_content = changed_content.replace('</p>', '&nbsp;</p>')
    # 토글을 기본 닫힌 상태로 표시하기 위해
    changed_content = changed_content.replace(
        'class="toggle"><li><details open=""><summary>', 'class="toggle"><li><details><summary>')
    # 마지막으로 changed_content 에서 <header> 태그까지 지워버림 (제목을 포함하여 페이지 Property가 적힌 테이블까지 전부 삭제)
    changed_content = changed_content.split(
        '<header')[0] + changed_content.split('</header>')[1]

    # Embed 링크 HTML 태그 변환
    changed_content = make_embed(changed_content)

    # 글 도입부에 페이지 데이터 추가
    add_content = '<p><mark class="highlight-gray">이 글은 2020년 3월 9일 이후 Notion→Tistory 프로젝트가 어느정도 완성된 후부터 조금씩 티스토리로 옮겨진 글입니다.<br>원문은 </mark><mark class="highlight-gray"><a href="https://www.notion.so/B-E-s-blog-5411e6109fd44724b0c45db9eeea36ad">제 노션 블로그</a></mark><mark class="highlight-gray">에서 보실 수 있습니다.</mark></p>' + \
        '<p>본 게시물은 Notion에서 ' + created_date + '에 생성된 페이지입니다.</p><p></p>'
    changed_content = changed_content.replace(
        '<div class="page-body">', '<div class="page-body">' + add_content)

    return changed_content


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Creating directory. " + directory)


def get_folder_name(url, title):
    max_cat_num = 0
    for folder in os.listdir(url):
        if os.path.splitext(folder)[1] == "" and folder[:2].isdecimal() and folder[2] == "_":
            if folder[3:] == title:
                return folder
            elif max_cat_num <= int(folder[:2]):
                max_cat_num += 1
    folder_name = str(max_cat_num).zfill(2) + "_" + title
    return folder_name


def get_category_name(html):
    split = html.split("</a></td></tr>")[0]
    num = split.rfind("</span>")
    return split[(num+7):]


def get_post_num(html):
    return html.split("Number in Project</th><td>")[1].split("</td>")[0].zfill(3)


def autoChange_HTML(file):  # 경로를 포함한 파일명
    html_file = open(file, "r", encoding='UTF8')
    file_content = html_file.read()

    category_name = get_category_name(file_content)
    post_num = get_post_num(file_content)
    new_content = change_content(file_content)
    page_title, new_file_name = search_page_title(file_content)
    folder_path = folder_destination + "\\"
    folder_path += get_folder_name(folder_destination, category_name)
    folder_path = folder_path + "\\" + post_num + \
        "_" + page_title.split(" -")[0] + "\\"
    createFolder(folder_path)
    print("thumbnail title is : ")
    print(extract_thumbnail_title(file_content))
    make_thumbnail(folder_path, extract_thumbnail_title(
        file_content), "#FFFFFF")

    # new_file_name을 파일명으로, folder_destination 경로에 UTF8로 인코딩해서 파일 생성
    new_html_file = open(folder_path + new_file_name +
                         ".html", "w", encoding='UTF8')
    new_txt_file = open(folder_path + new_file_name +
                        ".txt", "w", encoding='UTF8')

    # 생성된 파일에 new_content를 붙여넣음
    new_html_file.write(new_content)

    # 클립보드에 new_content를 저장. ctrl+v 만 누르면 바로 붙여넣기가 됨(편리!)
    clipboard.copy(page_title + "\n" + new_content)
    new_txt_file.write(page_title + "\n" + new_content)

    # 열었던 파일들 닫기
    html_file.close()
    new_html_file.close()
    new_txt_file.close()

    # 압축해제했던 원본 html 파일 제거
    os.remove(file)


class MyHandler(FileSystemEventHandler):
    # 파일이 생성되면
    def on_created(self, event):
        # 생성된 파일들
        for zip_file in os.listdir(folder_to_track):
            file_ext = os.path.splitext(zip_file)[1]
            # 생성된게 zip 파일이면
            if file_ext == '.zip':
                # 파일 이름(확장자 포함) 출력
                print(zip_file)
                # zip파일 읽기
                with zipfile.ZipFile(folder_to_track + "\\" + zip_file, "r") as zip_ref:
                    # 압축된 파일들(zip파일 내부 파일)
                    for innerFile in zip_ref.namelist():
                        # 우선 출력하고
                        print(innerFile)
                        innerFile_name, innerFile_ext = os.path.splitext(
                            innerFile)
                        # html 파일이면
                        if innerFile_ext == '.html':
                            # html 파일이라고 출력하고
                            print(innerFile_name + " is html file!")
                            # 압축파일에서 이 html 파일만 folder_destination 경로에 압축해재
                            #	(notion export에서 html은 하나만 나오므로 한번만 해주면 된다)
                            zip_ref.extract(innerFile, folder_destination)
                            print("extract success!")
                            print("reading......")

                            # html파일을 수정 및 원본 삭제, 파일내용 클립보드에 저장
                            autoChange_HTML(
                                folder_destination + "\\" + innerFile)

                        else:
                            # html 파일이 아닌 경우, 그냥 아니라고 출력
                            print(innerFile_name + "is not html file...")

                # 원본 압축파일, zip파일을 제거
                os.remove(folder_to_track + "\\" + zip_file)
                print("removed    " + zip_file)
                print("done.")


folder_to_track = 'notion'
folder_destination = 'tistory'
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()

try:
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    observer.stop()
    print("error")
observer.join()
