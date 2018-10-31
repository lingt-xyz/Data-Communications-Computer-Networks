import os
import json
import threading


class FileApp:
    lock = threading.Lock()

    def __init__(self):
        self.status = 400
        self.content_type = 'text/plain'
        self.content = ''

    def get_all_files(self, dir_url):
        files = FileApp.files_list_in_dir(dir_url)
        output = {}
        f_list = []
        for f in files:
            f_list.append(f)
        output['dir_url'] = dir_url
        output['files'] = f_list
        self.status = 200
        self.content = json.dumps(output)
        self.content_type = 'application/json'

    def get_content(self, dir_url, file_name):
        if file_name.find('../') != -1:
            output = {}
            output['warning'] = 400
            output['message'] = 'Bad Request - Can not access to outer dictionary'
            self.status = 400
            self.content = json.dumps(output)
            self.content_type = 'application/json'
        else:
            files = FileApp.files_list_in_dir(dir_url)
            if file_name not in files:
                output = {}
                output['error'] = 404
                output['message'] = 'Not found'
                self.status = 404
                self.content = json.dumps(output)
                self.content_type = 'application/json'
            else:
                FileApp.lock.acquire()
                try:
                    with open(dir_url + '/' + file_name, 'r', errors="ignore") as file_obj:
                        content = file_obj.read()
                finally:
                    FileApp.lock.release()

                self.status = 200
                self.content = content
                self.content_type = FileApp.get_content_type(file_name)

    def post_content(self, dir_url, file_name, content):
        FileApp.lock.acquire()
        try:
            with open(dir_url + '/' + file_name, 'w') as f:
                f.write(content)
        finally:
            FileApp.lock.release()

        self.status = 200
        self.content = 'write in to ' + dir_url + '/' + file_name
        self.content_type = 'text/plain'

    @staticmethod
    def get_content_type(file_name):
        content_type = 'text/plain'
        suffix = os.path.splitext(file_name)[-1]
        if suffix == '.json':
            content_type = 'application/json'
        if suffix == '.html':
            content_type = 'text/html'
        if suffix == '.xml':
            content_type = 'text/xml'
        return content_type

    @staticmethod
    def files_list_in_dir(dir_url):
        files_lst = []

        for root, dirs, files in os.walk(dir_url):
            for file in files:
                temp = root + '/' + file
                files_lst.append(temp[(len(dir_url) + 1):])

        return files_lst
