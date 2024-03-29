import socket
from urllib.parse import urlparse
import re
import MockHttpClient

class Parameter:
    url = None
    verbose = False
    headers = None
    bodyData = None
    writeFileName = None
    port = 80
    
    @staticmethod
    def reInit():
        Parameter.url = None
        Parameter.verbose = False
        Parameter.headers = None
        Parameter.bodyData = None
        Parameter.writeFileName = None


def writeFile(fileName, content):
    with open(fileName, 'w') as f:
            f.write(content)
    print("Write reponse to the file: " + fileName)

def showHelpMenu():
    print("httpc is a curl-like application but supports HTTP protocol only." + "\n" +
          "Usage: " + "\n" +
          "httpc command [arguments]" + "\n" +
          "The commands are: " + "\n" +
          "get    executes a HTTP GET request and prints the response." + "\n" +
          "post   executes a HTTP POST request and prints the resonse." + "\n" +
          "help   prints this screen." + "\n")


def sendHttpRequest(command):
    if ("-o" in command):
        Parameter.writeFileName = command.split(" -o ")[1]
        command = command.split(" -o ")[0]
    if ("-v" in command):
        Parameter.verbose = True
    if ("-h" in command):
        Parameter.headers = getHeaders(command)

    urlString = command.split(" ")[-1]
    if("'" in urlString):
        Parameter.url = urlString[1:-1]
    else:
        Parameter.url = urlString
    
    # Get Usage: httpc get [-v] [-h key:value] URL
    # Post Usage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL
    if (command.startswith("get") or command.startswith("post")):
        o = urlparse(Parameter.url)
        host = o.hostname
        if(o.port is None):
            port = Parameter.port
        else:
            port = o.port
        while(True):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))

                if(command.startswith("post")):
                    if ("-d" in command and "-f" not in command):
                        infos = command.split(" -d ")[1].split(" ")
                        Parameter.bodyData = (infos[0] + infos[1])[1:-1]
                    if ("-f" in command and "-d" not in command):
                        readFileName = command.split(" -f ")[1].split(" ")[0]
                        with open(readFileName, 'r') as f:
                            Parameter.bodyData = f.read()
                    request = MockHttpClient.HttpRequest(host, o.path, Parameter.bodyData, Parameter.headers)
                    #print(request.getPost().decode('utf-8'))
                    s.sendall(request.getPost())

                else:
                    request = MockHttpClient.HttpRequest(host, o.path, o.query, Parameter.headers)
                    #print(request.getGet().decode('utf-8'))
                    s.sendall(request.getGet())
                data = recvall(s)
            response = MockHttpClient.HttpResponse(data)

            if(response.code == MockHttpClient.HttpCode.redirect):
                host = response.location
            else:
                break

        if Parameter.verbose:
            print(response.text)
            if(Parameter.writeFileName != None):
                writeFile(Parameter.writeFileName, response.text)
        else:
            print(response.body)
            if(Parameter.writeFileName != None):
                writeFile(Parameter.writeFileName, response.text)

    # Invaid
    else:
        print("Invalid command.")


def getHeaders(command):
    pairs = re.findall("-h (.+?:.+?) ", command)
    return "\r\n".join(pairs)
    #return command.split(" -h ")[1].split(" ")[0]

def recvall(sock):
    BUFF_SIZE = 1024 # 1 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data

def execute(command):
    if ("help" in command):
        showHelpMenu()
    else:
        sendHttpRequest(command)


# program entrance
while True:
    command = input("\nplease enter the command; enter 'quit' or 'exit' or 'bye' to quit:\n" + "httpc ")
    if("quit" in command or "exit" in command or "bye" in command):
        break
    
    Parameter.reInit()
    execute(command)
