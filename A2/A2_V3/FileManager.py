import os
import json
import threading
import logging


class FileManager:
    lock = threading.Lock()

    def __init__(self):
        self.status = 400
        self.content = ''

    def get_all_files(self, dir_url, content_type):
        files = FileManager.files_list_in_dir(dir_url)
        output = {}
        f_list = []
        for f in files:
            f_list.append(f)
        self.status = 200
        self.content = FileManager.generate_content(content_type, f_list)
        #output['files'] = f_list
        #self.content = json.dumps(output)

    def get_content(self, dir_url, file_name, content_type):
        if file_name.find('../') != -1:
            output = {}
            output['warning'] = 400
            output['message'] = 'Bad Request - Can not access to outer dictionary'
            self.status = 400
            self.content = json.dumps(output)
        else:
            files = FileManager.files_list_in_dir(dir_url)
            if file_name not in files:
                output = {}
                output['error'] = 404
                output['message'] = 'Not found'
                self.status = 404
                self.content = json.dumps(output)
            else:
                FileManager.lock.acquire()
                try:
                    with open(dir_url + '/' + file_name, 'r', errors="ignore") as file_obj:
                        content = file_obj.read()
                finally:
                    FileManager.lock.release()

                self.status = 200
                self.content = content

    def post_content(self, dir_url, file_name, content, content_type):
        if(content_type == "application/json"):
            logging.debug("Decode string:{} to JSON.".format(content))
            values = json.loads(content)
            for key, value in values.items():
                content = value
        FileManager.lock.acquire()
        try:
            with open(dir_url + '/' + file_name, 'w') as f:
                f.write(content)
        finally:
            FileManager.lock.release()

        self.status = 200
        #self.content = 'write in to ' + dir_url + '/' + file_name
        self.content = json.dumps("")

    @staticmethod
    def generate_content(content_type, content_list):
        if content_type == 'application/json':
            output = {}
            output[""] = content_list
            return json.dumps(output)
        elif content_type == 'text/xml':
            return FileManager.generate_xml(content_list)

    @staticmethod
    def generate_xml(file_list):
        xml = "<root>"
        for value in file_list:
            xml += ("<file>"+value+"</file>")
        xml += "</root>"
        return xml

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
