import socket
import threading
import logging
import re
from pprint import pprint
#from MockHttpRequest import MockHttpRequest
#from MockHttpResponse import MockHttpResponse

from FileManager import FileManager

class MockHttpServer:

	BUFFER_SIZE = 1024 # 1 KiB
	#HOST = 'localhost'

	# initialized port and data directory
	def __init__(self, port=8080, d="."):
		self.port = port
		self.dataDirectory = d

	# start the server and dispatch new connection to a thread to handle the communication between client and server
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
				threading.Thread(target=self.handler, args=(conn, address, self.dataDirectory)).start()

		finally:
			logging.info("Shuting down the server...")
			listener.close()
			logging.info('Web server has been shut down at {}.'.format(self.port))

	# handle the request from client and return the response to client
	def handler(self, conn, address, dirPath):
		try:
			# convert bytes to string
			data = self.recvall(conn).decode("utf-8")
			logging.debug("Received the data: \r\n{0}".format(data))
			requestParser = HttpRequestParser(data)
			logging.debug("Received the {0} request.".format(requestParser.method))
			# pprint(vars(requestParser))
			response_msg = self.generateResponse(requestParser, dirPath)
			logging.debug('Response message: {0}.'.format(response_msg))
			conn.send(response_msg)
			#conn.send('HTTP/1.1 200 OK\r\n\r\nsomething'.encode("utf-8"))
			conn.close()
		except IOError as e:
			logging.err(e)
		finally:
			conn.close()
			logging.debug("Disconnected from {0}.".format(address))

	# read all content from client
	def recvall(self, conn):
		data = b''
		while True:
			part = conn.recv(self.BUFFER_SIZE)
			data += part
			if len(part) < self.BUFFER_SIZE:
				# either 0 or end of data
				break
		return data

	# deal the file request, generate response bytes string, according to HTTP standards.
	def generateResponse(self, requestParser, dirPath):
		if requestParser.method == HttpMethod.Download:
			status = 200
			# TODO set header: Content-Disposition: attachment
		elif requestParser.method == HttpMethod.GetResource:
			status = 200
			content = "" # TODO			
			
		elif requestParser.method == HttpMethod.PostResource:
			status = 200
			content = "" # TODO

		else:
			# file app logic
			fileapp = FileManager()

			if requestParser.method == HttpMethod.Get:
				if requestParser.operation == Operation.GetFileList:
					fileapp.get_all_files(dirPath, requestParser.contentType)	
				elif requestParser.operation == Operation.GetFileContent:
					fileapp.get_content(dirPath, requestParser.fileName, requestParser.contentType)
			
			elif requestParser.method == HttpMethod.Post:
				fileapp.post_content(dirPath, requestParser.fileName, requestParser.fileContent, requestParser.contentType)

			status = fileapp.status
			content = fileapp.content

		# response
		response_msg = 'HTTP/1.1 ' + str(status) + ' ' + self.status_phrase(status) + '\r\n'
		response_msg = response_msg + 'Connection: close\r\n' + 'Content-Length: ' + str(len(content)) + '\r\n'
		response_msg = response_msg + 'Content-Type: ' + requestParser.contentType + '\r\n\r\n'
		response_msg = response_msg + content
		return response_msg.encode("utf-8")

	# HTTP status code
	def status_phrase(self, status):
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

'''
get 'http://google.ca/'
---------------------------------
GET /? HTTP/1.0
Host:google.ca


get 'http://google.ca/foo'
---------------------------------
GET /foo? HTTP/1.0
Host:google.ca

get -h Content-Type:application/json 'http://google.ca/foo'
'''

'''
post -h Content-Type:application/json -h hk1:hv1 -d '{"": 123abc}' http://httpbin.org/filename
--------------------------------------------------------------------------------------------------
POST /filename HTTP/1.0
Content-Type:application/json
hk1:hv1
Content-Length: 11
Host: httpbin.org
User-Agent: Concordia-HTTP/1.0
Connection: close

{"":123abc}


'''

class HttpRequestParser:
	def __init__(self, data):
		self.contentType = "application/json"
		self.contentDisposition = "inline"

		(http_header, http_body) = data.split('\r\n\r\n')
		lines = http_header.split('\r\n')
		(method, resource, version) = lines[0].split(' ')

		for line in lines:
			if("Content-Type" in line):
				self.contentType = line.split(':')[1]

		if(resource.endswith("?")):
			resource = resource[:-1]
		if(method == HttpMethod.Get):
			self.method = HttpMethod.Get
			if(resource == "/get" ):
				self.operation = Operation.GetResource
			elif(resource == "/download" ):
				self.operation = Operation.Download
			elif(resource == "/" ):
				self.operation = Operation.GetFileList
			else:
				m = re.match(r"/(.+)", resource)
				if(m):
					self.operation = Operation.GetFileContent
					self.fileName = m.group(1)
				else:
					self.operation = Operation.Invalid
		elif(method == HttpMethod.Post):
			self.method = HttpMethod.Post
			m = re.match(r"/(.+)", resource)
			if(m):
				self.fileContent = http_body
				if(m.group(1) == "post"):
					self.operation = Operation.PostResource
				else:				
					self.operation = Operation.WriteFileContent
					self.fileName = m.group(1)
			else:
				self.operation = Operation.Invalid			
		else:
			self.method = HttpMethod.Invalid
		self.version = version
		self.contentDisposition = None # TODO
		self.overwrite = False # TODO



class HttpMethod:
	Invalid = "Invalid"
	Get = "GET"
	Post = "POST"

class Operation:
	Invalid = 0
	GetFileList = 1
	GetFileContent = 2
	WriteFileContent = 3
	GetResource = 4
	PostResource = 5
	Download = 6
