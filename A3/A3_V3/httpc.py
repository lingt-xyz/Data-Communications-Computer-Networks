import socket
from urllib.parse import urlparse
import re
from MockHttpClient import *
from UdpController import *
import logging
import sys
import argparse


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
            udpClient = UdpController()
            udpClient.connectServer()
            if(command.startswith("post")):
                if ("-d" in command and "-f" not in command):
                    infos = command.split(" -d ")[1].split(" ")
                    Parameter.bodyData = (infos[0] + infos[1])[1:-1]
                if ("-f" in command and "-d" not in command):
                    readFileName = command.split(" -f ")[1].split(" ")[0]
                    with open(readFileName, 'r') as f:
                        Parameter.bodyData = f.read()
                request = HttpRequest(host, o.path, Parameter.bodyData, Parameter.headers)
                #print(request.getPost().decode('utf-8'))
                logging.debug("[Application] Client sent request: {}".format(request.getPost()))
                udpClient.sendMessage(request.getPost())

            else:
                request = HttpRequest(host, o.path, o.query, Parameter.headers)
                logging.debug("[Application] Client sent request: {}".format(request.getGet()))
                udpClient.sendMessage(request.getGet())
            data = udpClient.receiveMessage()
            if data is None:
                logging.debug("[Application] Client did not receive response.")
                sys.exit(0)
            logging.debug("[Application] Client received response: {}".format(data.decode('utf-8')))
                
            response = HttpResponse(data)
            if(response.code == HttpCode.redirect):
                host = response.location
            else:
                break

        udpClient.dis_connect()

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
# parse the input parameters
parser = argparse.ArgumentParser()
parser.add_argument("-v", help="output log", action='store_true')
args = parser.parse_args()

# whether output debug
if (args.v):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
else:
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

while True:
    command = input("\nplease enter the command; enter 'quit' or 'exit' or 'bye' to quit:\n" + "httpc ")
    if("quit" in command or "exit" in command or "bye" in command):
        break

    Parameter.reInit()
    execute(command)
