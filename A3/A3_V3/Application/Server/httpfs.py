from Application.Server.httpserver import MockHttpServer
import sys
import logging
import argparse

'''
# Usage: python3 httpfs [-v] [-p PORT] [-d PATH-TO-DIR]
'''

# parse the input parameters
parser = argparse.ArgumentParser()
parser.add_argument("-v", help="output log", action='store_true')
parser.add_argument("-p", help="server port", type=int, default=8080)
parser.add_argument("-d", help="data directory", default=".")
args = parser.parse_args()

# whether output debug
if (args.v):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
else:
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# start the server
server = MockHttpServer(args.p, args.d)
server.start()
