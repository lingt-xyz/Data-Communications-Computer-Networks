import socket
import threading

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
				threading.Thread(target=self.response, args=(client, address)).start()
		finally:
			print("Shuting down the server...")
			listener.close()
			print('Web server is shut down at', self.port)

	def response(self, client, address):
		data = self.recvall(client).decode("utf=8")
		print(data)
		(http_header, http_body) = data.split('\r\n\r\n')
		lines = http_header.split('\r\n')
		(method, resource, http_version) = lines[0].split(' ')
		# do we need Content-Type? json, xml, plain
		if(method == "GET"):
			print("GET")
		elif(method == "POST"):
			print("POST")
		else:
			print("Unsupported.")
		
	def recvall(self, client):
		data = b''
		while True:
			part = client.recv(self.BUFFER_SIZE)
			data += part
			if len(part) < self.BUFFER_SIZE:
				# either 0 or end of data
				break
		return data


server = MockHttpServer()
server.start()
