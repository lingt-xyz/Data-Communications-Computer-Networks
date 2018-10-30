import socket
import threading
import logging, sys
# from fileType import dealFile

class MockHttpServer:

	BUFFER_SIZE = 1024 # 1 KiB
	#HOST = 'localhost'

	def __init__(self, port=8080):
		self.port = port
		self.webRoot = 'data'

	def start(self):
		print("Starting web server...")
		listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			listener.bind(('', self.port))
			listener.listen(5)
			print('Web server is listening at', self.port)
			while True:
				(client, address) = listener.accept()
				logging.debug("Received a connection from {0}".format(address))
				threading.Thread(target=self.response, args=(client, address)).start()

		finally:
			print("Shuting down the server...")
			listener.close()
			print('Web server has been shut down at', self.port)

	def response(self, client, address):
		# convert bytes to string
		data = self.recvall(client).decode("utf-8")
		logging.debug("Received the data: \r\n{0}".format(data))
		(http_header, http_body) = data.split('\r\n\r\n')
		lines = http_header.split('\r\n')
		(method, resource, http_version) = lines[0].split(' ')
		# do we need Content-Type? json, xml, plain
		logging.debug("Received the {0} request.".format(method))
		if(method == "GET"):
			logging.debug("Received the GET request.")
			if(resource == "/"):
				logging.debug("Get file list")
			elif(resource == ""):# /foo
				logging.debug("Get file content")
			else:
				logging.error("Unsupported request.")
		elif(method == "POST"):
			logging.debug("Received the POST request.")
		else:
			logging.error("Unsupported Method.")

	# read all content from client
	def recvall(self, client):
		data = b''
		while True:
			part = client.recv(self.BUFFER_SIZE)
			data += part
			if len(part) < self.BUFFER_SIZE:
				# either 0 or end of data
				break
		return data

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
server = MockHttpServer()
server.start()
