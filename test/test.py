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


folder_to_track = 'notion'
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()

try:
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    observer.stop()
    print("\n<error>")
observer.join()
