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

class HttpRequest:

  def __init__(self, host, path, query, headers):
    self.path = path
    self.host = host
    self.query = query
    self.headers = headers

  def getGet(self):
    headers = ( "GET "+ self.path + "?" + self.query + " HTTP/1.0\r\n"
                "{headers}\r\n"
                "Host:" + self.host + "\r\n\r\n")
    header_bytes = headers.format(
        headers=self.headers
    ).encode('utf-8')
    return  header_bytes

  def getPost(self):
    headers = ( "POST {path} HTTP/1.0\r\n"
                "{headers}\r\n"
                "Content-Length: {content_length}\r\n"
                "Host: {host}\r\n"
                "User-Agent: Concordia-HTTP/1.0\r\n"
                "Connection: close\r\n\r\n")

    body_bytes = self.query.encode('utf-8')                              
    header_bytes = headers.format(
        path=self.path,
        headers=self.headers,
        content_length=len(self.query),
        host=self.host
    ).encode('utf-8')
    return header_bytes + body_bytes


class HttpResponse:

  def __init__(self, response):
    self.text = response.decode('utf-8')
    self.parseText()

  def parseText(self):
    texts = self.text.split("\r\n\r\n")
    self.header = texts[0]
    self.body = texts[1]
    lines = self.header.split("\r\n")
    infos = lines[0].split(" ")
    self.code = infos[1]
    self.status = infos[2]
    if(self.code == HttpCode.redirect):
      self.location = lines[1].split(" ")[1].split("//")[1][:-1]
      print("Redirect to " + self.location)


class HttpCode:
  redirect = "301"
  ok = "200"
