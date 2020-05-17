# python 3.7.6
# python 3.8.2

# pip install watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import time

import os
# pip install zipfile
import zipfile
# pip install clipboard
import clipboard

import urllib


def search_page_title(file_content):
    # html 파일에서 <h1 class="page-title"> 태그 안에 있는 제목을 꺼내서 ".html"이라고 확장자명을 추가하여 new_name 에 저장
    title = file_content.split('<h1 class="page-title">')[1].split('</h1>')[0]
    # page_title 예외처리.. 제목에 소괄호()가 있으면 <mark> 태그가 붙어있음.
    # mark 태그를 제거
    title = title.replace("<mark class=\"highlight-gray\">",
                          "").replace("</mark>", "")
    file_name = title.split(' - ')[0] + ".html"
    return title, file_name


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

    return changed_content


def autoChange_HTML(file):  # 경로를 포함한 파일명
    html_file = open(file, "r", encoding='UTF8')
    file_content = html_file.read()

    new_content = change_content(file_content)
    page_title, new_file_name = search_page_title(file_content)

    # new_file_name을 파일명으로, folder_destination 경로에 UTF8로 인코딩해서 파일 생성
    new_html_file = open(folder_destination +
                         new_file_name, "w", encoding='UTF8')

    # 생성된 파일에 new_content를 붙여넣음
    new_html_file.write(new_content)

    # 클립보드에 new_content를 저장. ctrl+v 만 누르면 바로 붙여넣기가 됨(편리!)
    clipboard.copy(page_title + "\n" + new_content)

    # 열었던 파일들 닫기
    html_file.close()
    new_html_file.close()

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
                print("removed " + zip_file)
                print("done.")


folder_to_track = 'notion'
folder_destination = 'export'
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
