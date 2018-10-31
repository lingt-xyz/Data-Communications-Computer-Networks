
from MockHttpServer import MockHttpServer
import sys
import logging
import argparse



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