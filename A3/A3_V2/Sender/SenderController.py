from socket import *
from DealPackets.Packet import *
from Sender.SenderWindow import *
from DealPackets.packetConstructor import *


class SenderController:
    __window = None
    __socket = None
    __addr = None
    __routerAddr = None
    __packetBuilder = None
    __port = None

    def __init__(self, ip, port):
        if (str(ip).lower() == const.LOCAL_HOST_ALIAS):
            ip = const.LOCAL_HOST_IP
        self.__addr = (ip, port)
        self.__routerAddr = (const.LOCAL_HOST_IP, const.ROUTER_PORT)
        self.__packetBuilder = PacketConstructor(ip,port)

    """
    The client invoke this function to send http request
    """
    def sendMessage(self, message):
        #self.__socket = socket(AF_INET, SOCK_DGRAM)
        #self.__socket.settimeout(1)
        self.__window = SenderWindow(message, self.sendPacket, self.getResponse)

        if self.connect(self.__window.windowSize):
            print("Connected")

            while not self.__window.finished():
                self.__window.process()
        else:
            print("Can't establish connection")

        self.__port = self.__socket.getsockname()[1]
        self.__socket.close()

    def sendPacket(self, packetType, sequenceNumber, content):
        print("Sending packet type: " + str(packetType) + " with #" + str(sequenceNumber))
        packet = self.__packetBuilder.build(packetType, sequenceNumber, content)
        self.__socket.sendto(packet.getBytes(), self.__routerAddr)

    def getResponse(self):
        self.__socket = socket(AF_INET, SOCK_DGRAM)
        self.__socket.settimeout(1)


    def connect(self, windowSize):
        #TODO:
        self.__socket = socket(AF_INET, SOCK_DGRAM)
        self.__socket.settimeout(1)

    def getSocketPort(self):
        return self.__port
