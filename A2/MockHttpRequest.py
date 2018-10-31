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

import re

class MockHttpRequest:
	def __init__(self, data):
		(http_header, http_body) = data.split('\r\n\r\n')
		lines = http_header.split('\r\n')
		(method, resource, version) = lines[0].split(' ')

		if(method == HttpMethod.Get):
			self.method = HttpMethod.Get
			if(resource == "/?"):
				self.operation = Operation.GetFileList
			else:
				m = re.match(r"/([\w_]+)\?", resource)
				if(m):
					self.operation = Operation.GetFileContent
					self.fileName = m.group(1)
				else:
					self.operation = Operation.Invalid
		elif(method == HttpMethod.Post):
			self.method = HttpMethod.Post
			m = re.match(r"/([\w_]+)", resource)
			if(m):
				self.operation = Operation.WriteFileContent
				self.fileName = m.group(1)
				self.fileContent = http_body
				self.contentType = "application/json"
				self.contentDisposition = "inline"
				for line in lines:
					if("Content-Type" in line):
						self.contentType = line.split(':')[1]
					if("Content-Disposition" in line):
						self.contentDisposition = line.split(':')[1]
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
