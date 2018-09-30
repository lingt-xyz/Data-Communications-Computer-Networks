

import socket
from urllib.parse import urlparse
# The URL parsing functions focus on splitting a URL string into its components


class Method:
    url_info = None
    host = None
    port = None
    path = None
    query = None
    http_version = " HTTP/1.1\r\n"
    new_url = None

    def __init__(self, url):

        self.url_info = urlparse(url)
        self.host = self.url_info.hostname
        self.port = 80
        self.path = self.url_info.path
        self.query = "?" + self.url_info.query #? signify the value of

        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.host, self.port))

    def http_get(self, command, key, value, writefile):

        request_line = "GET " + str(self.path) + str(self.query) + self.http_version  #a string
        hostheader = "Host: " + str(self.host) + "\r\n\r\n"
        request_msg = request_line + hostheader

        """
        deal with the request associate with the headers
        """
        if "-h" in command:
            hostheader = "Host: " + str(self.host) + "\r\n"
            kv = key + value + "\r\n\r\n"
            request_msg = request_line + hostheader + kv #request msg is the msg you send to server, it can appear and be printed

        request_msg = request_msg.encode("utf-8")
        self.conn.sendall(request_msg) #send the msg

        response = self.conn.recv(1024)
        response = response.decode('utf-8')

        """
        show the verbose content or not 
        """
        if "-v" in command:
            if ("-o" not in command):
                print(response)
            elif ("-o" in command):

                self.writetofile(writefile, response)
                print("test")

        # not showing the verbose headers
        else:
            message_pos = response.find('\r\n\r\n')
            if (message_pos >= 0):
                response = response[message_pos + 4:]
                if ("-o" not in command):
                    print(response)
                elif ("-o" in command):
                    self.writetofile(writefile, response)

    def http_post(self, command, key, value, data, writefile):

        request_line = "POST " + str(self.path) + self.http_version
        hostheader = "Host: " + str(self.host) + "\r\n"
        kv = key + value + "\r\n"
        cl = cl_headerline = "Content-Length: " + str(len(data)) + "\r\n\r\n"
        request_msg = request_line + hostheader + kv + cl + data

        request_msg = request_msg.encode("utf-8")
        self.conn.sendall(request_msg)

        response = self.conn.recv(1024)
        response = response.decode('utf-8')

        """
        show the verbose content or not 
        """
        if "-v" in command:
            if ("-o" not in command):
                print(response)
            elif ("-o" in command):
                self.writetofile(writefile, response)


        # not showing the verbose headers
        else:
            message_pos = response.find('\r\n\r\n')
            if (message_pos >= 0):
                response = response[message_pos + 4:] #pos?
                if ("-o" not in command):
                    print(response)
                elif ("-o" in command):
                    self.writetofile(writefile, response)

    def redirect(self):

        request_msg = "GET " + self.path + self.query + self.http_version + "Host: " + str(self.host) + "\r\n\r\n"
        request_msg = request_msg.encode("utf-8")

        self.conn.sendall(request_msg)

        response = self.conn.recv(1024)
        response = response.decode('utf-8')
        print(response)
        self.new_url = self.fetchnewurl(response)

    def fetchnewurl(self, response):

        newurl_pos = response.find("http:")
        Access_pos = response.find("Access-Control") - 2
        return response[newurl_pos:Access_pos]

    def getnewurl(self):

        return self.new_url

    def writetofile(self, file, r):

        with open(file, 'w') as f:
            f.write(r)
        print("Reponse wirte to the file" + file)





















