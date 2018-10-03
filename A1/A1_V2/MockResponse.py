"""
HTTP/1.0 301 Moved Permanently
Location: http://www.google.ca/
Content-Type: text/html; charset=UTF-8
Date: Wed, 03 Oct 2018 19:51:01 GMT
Expires: Fri, 02 Nov 2018 19:51:01 GMT
Cache-Control: public, max-age=2592000
Server: gws
Content-Length: 218
X-XSS-Protection: 1; mode=block
X-Frame-Options: SAMEORIGIN

<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>301 Moved</TITLE></HEAD><BODY>
<H1>301 Moved</H1>
The document has moved
<A HREF="http://www.google.ca/">here</A>.
</BODY></HTML>
"""

"""
HTTP/1.1 200 OK
Connection: close
Server: gunicorn/19.9.0
Date: Wed, 03 Oct 2018 20:08:34 GMT
Content-Type: application/json
Content-Length: 245
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
Via: 1.1 vegur

{
  "args": {
    "assignment": "1", 
    "course": "networking"
  }, 
  "headers": {
    "Connection": "close", 
    "Host": "httpbin.org"
  }, 
  "origin": "206.180.247.122", 
  "url": "http://httpbin.org/get?course=networking&assignment=1"
}
"""
class HttpResponse:
  def __init__(response):
    self.text = response.decode('utf-8')
    self.parseText()

  def parseText():
    texts = self.text.split("\r\n\r\n")
    self.header = texts[0]
    self.body = texts[1]
    lines = self.header.split("\r\n")
    infos = lines[0].split(" ")
    self.code = infos[1]
    self.status = infos[2]
    self.location = lines[1]
