import socket
import threading
import logging
from pprint import pprint
#from MockHttpRequest import MockHttpRequest
#from MockHttpResponse import MockHttpResponse

from FileManager import FileManager

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

	def handler(conn, is_v, dirPath):
		try:
			if is_v:
				logging.info('*** receive a new request')
			request = conn.recv(1024).decode("utf-8")
			if is_v:
				logging.info('* raw request:' + request)

			# parse the request message
			rqstIndex = request.find('\r\n')
			requestLine = request[:rqstIndex]
			if is_v:
				logging.info('* request line:' + requestLine)
			rqstIndexContents = requestLine.split()
			rqstMethod = rqstIndexContents[0]
			rqstUrl = rqstIndexContents[1]
			if is_v:
				logging.info('* request method:' + rqstMethod)
				logging.info('* request url:' + rqstUrl)
			bodyIndex = request.find('\r\n\r\n') + 4
			bodyContent = request[bodyIndex:]
			if is_v:
				logging.info('* body content:' + bodyContent)

			# default value
			status = 0
			content = ''
			contentType = ''

			# file app logic
			if rqstMethod == 'GET':
				if rqstUrl == '/':
					fileapp = FileManager()
					fileapp.get_all_files(dirPath)
					status = fileapp.status
					content = fileapp.content
					contentType = fileapp.content_type
				else:
					fileapp = FileManager()
					fileName = rqstUrl[1:]
					fileapp.get_content(dirPath, fileName)
					status = fileapp.status
					content = fileapp.content
					contentType = fileapp.content_type

			elif rqstMethod == 'POST':
				fileapp = FileManager()
				fileName = rqstUrl[1:]
				fileapp.post_content(dirPath, fileName, bodyContent)
				if -is_v:
					logging.info('*body-content:' + bodyContent)
				status = fileapp.status
				content = fileapp.content
				contentType = fileapp.content_type

			# response
			# gmt_format = '%a, %d %b %Y %H:%M:%S GMT'
			response_msg = 'HTTP/1.1 ' + str(status) + ' ' + status_phrase(status) + '\r\n'
			response_msg = response_msg + 'Connection: close\r\n' + 'Content-Length: ' + str(len(content)) + '\r\n'
			response_msg = response_msg + 'Content-Type: ' + contentType + '\r\n\r\n'
			response_msg = response_msg + content
			if is_v:
				logging.info('*response msg:' + response_msg)
			conn.sendall(response_msg.encode("utf-8"))

		except IOError as e:
			if is_v:
				print(e)
		finally:
			conn.close()


def status_phrase(status):
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