import socket
import threading
import logging
from pprint import pprint
from MockHttpRequest import MockHttpRequest
#from MockHttpResponse import MockHttpResponse

# from fileType import dealFile

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
				(client, address) = listener.accept()
				logging.debug("Received a connection from {0}.".format(address))
				threading.Thread(target=self.response, args=(client, address)).start()

		finally:
			logging.info("Shuting down the server...")
			listener.close()
			logging.info('Web server has been shut down at {}.'.format(self.port))

	def response(self, client, address):
		# convert bytes to string
		data = self.recvall(client).decode("utf-8")
		logging.debug("Received the data: \r\n{0}".format(data))
		request = MockHttpRequest(data)
		logging.debug("Received the {0} request.".format(request.method))
		pprint(vars(request))
		client.send('HTTP/1.1 200 OK\r\n\r\nsomething'.encode("utf-8"))
		client.close()

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
