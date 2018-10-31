import socket
import threading
import logging, sys
import argparse

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




# Usage: python3 httpfs [-v] [-p PORT] [-d PATH-TO-DIR]
parser = argparse.ArgumentParser()
parser.add_argument("-v", help="output log", action='store_true')
parser.add_argument("-p", help="server port", type=int, default=8080)
parser.add_argument("-d", help="data directory", default=".")
args = parser.parse_args()
#run_client(args.host, args.port)

if(args.v):# output debug
	logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
else:
	logging.basicConfig(stream=sys.stdout, level=logging.INFO)
server = MockHttpServer(args.p, args.d)
server.start()