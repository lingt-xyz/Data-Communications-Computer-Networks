from socket import *
from DealPackets.Packet import *
from Sender.SelectiveRepeatSender import *
from DealPackets.packetConstructor import *


class SenderController:
    __window = None
    __socket = None
    __addr = None
    __routerAddr = ('127.0.0.0', 3000)
    __packetBuilder = None
    __port = None

    def __init__(self, ip, port):
        if (str(ip).lower() == "localhost"):
            ip = "127.0.0.0"

        self.__packetBuilder = PacketConstructor(ip,port)
        self.__addr = (ip, port)

    def sendMessage(self, message):
        self.__socket = socket(AF_INET, SOCK_DGRAM)
        self.__socket.settimeout(1)
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
        #TODO:

    def connect(self, windowSize):
        #TODO:

    def getSocketPort(self):
        return self.__port
