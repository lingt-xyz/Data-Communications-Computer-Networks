import socket
import threading
import logging
from pprint import pprint
#from MockHttpRequest import MockHttpRequest
#from MockHttpResponse import MockHttpResponse

from dealFile import FileApp

class MockHttpServer:

	BUFFER_SIZE = 1024 # 1 KiB
	#HOST = 'localhost'

	def __init__(self, port=8080, d="."):
		self.port = port
		self.dataDirectory = d

	def start(self):
		logging.info("Starting web server...")
		listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			listener.bind(('', self.port))
			listener.listen(5)
			logging.info('Web server is listening at {}.'.format(self.port))
			while True:
				(conn, address) = listener.accept()
				logging.debug("Received a connection from {0}.".format(address))
				threading.Thread(target=self.response, args=(conn, address)).start()

		finally:
			logging.info("Shuting down the server...")
			listener.close()
			logging.info('Web server has been shut down at {}.'.format(self.port))

	def handler(conn, is_v, dir_path):
		try:
			if is_v:
				print('*** receive a new request')
			request = conn.recv(1024).decode("utf-8")
			if is_v:
				print('* raw request:' + request)

			# parse the request message
			reqst_index = request.find('\r\n')
			request_line = request[:reqst_index]
			if is_v:
				print('* request line:' + request_line)
			reqst_index_contents = request_line.split()
			reqst_method = reqst_index_contents[0]
			reqst_url = reqst_index_contents[1]
			if is_v:
				print('* request method:' + reqst_method)
				print('* request url:' + reqst_url)
			body_index = request.find('\r\n\r\n') + 4
			body_content = request[body_index:]
			if is_v:
				print('* body content:' + body_content)

			# default value
			status = 0
			content = ''
			content_type = ''

			# file app logic
			if reqst_method == 'GET':
				if reqst_url == '/':
					fileapp = FileApp()
					fileapp.get_all_files(dir_path)
					status = fileapp.status
					content = fileapp.content
					content_type = fileapp.content_type
				else:
					fileapp = FileApp()
					file_name = reqst_url[1:]
					fileapp.get_content(dir_path, file_name)
					status = fileapp.status
					content = fileapp.content
					content_type = fileapp.content_type

			elif reqst_method == 'POST':
				fileapp = FileApp()
				file_name = reqst_url[1:]
				fileapp.post_content(dir_path, file_name, body_content)
				if -is_v:
					print('*body-content:' + body_content)
				status = fileapp.status
				content = fileapp.content
				content_type = fileapp.content_type

			# response
			# gmt_format = '%a, %d %b %Y %H:%M:%S GMT'
			resp_msg = 'HTTP/1.1 ' + str(status) + ' ' + status_phrase_maping(status) + '\r\n'
			resp_msg = resp_msg + 'Connection: close\r\n' + 'Content-Length: ' + str(len(content)) + '\r\n'
			resp_msg = resp_msg + 'Content-Type: ' + content_type + '\r\n\r\n'
			resp_msg = resp_msg + content
			if is_v:
				print('*response msg:' + resp_msg)
			conn.sendall(resp_msg.encode("utf-8"))

		except IOError as e:
			if is_v:
				print(e)
		finally:
			conn.close()


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