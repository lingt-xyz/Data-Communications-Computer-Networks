
from MockHttpRequest import MockHttpRequest
from dealFile import FileApp


def status_phrase_maping(status):
    phrase = ''
    if status == 200:
        phrase = 'OK'
    if status == 301:
        phrase = 'Moved Permanently'
    if status == 400:
        phrase = 'Bad Request'
    if status == 404:
        phrase = 'Not Found'
    if status == 505:
        phrase = 'HTTP Version Not Supported'
    return phrase


def handler(conn, is_v, dir_path):



        requset = MockHttpRequest()
        # response
        # gmt_format = '%a, %d %b %Y %H:%M:%S GMT'
        resp_msg = 'HTTP/1.1 ' + str(requset.) + ' ' + status_phrase_maping(status) + '\r\n'
        resp_msg = resp_msg + 'Connection: close\r\n' + 'Content-Length: ' + str(len(requset.fileContent)) + '\r\n'
        resp_msg = resp_msg + 'Content-Type: ' + requset.contentType + '\r\n\r\n'
        resp_msg = resp_msg + requset.fileContent
        print('*response msg:'+resp_msg)
        conn.sendall(resp_msg.encode("utf-8"))


