from socket import *
from DealPackets.Packet import *
from DealPackets.PacketDecoder import *
from DealPackets.PacketBuilder import *
from Receiver.ReceiverWindow import *


class ReceiverController:
    address = None
    __socketRC = None
    __routerAddr = ('127.0.0.1', 3000)
    __packetBuilder = None
    __window = None
    __port = None

    def __init__(self, port):
        self.__port = port

    def sendPacket(self, packetType, sequenceNumber, content):
        print("Sending packet type: " + str(packetType) + " with #" + str(sequenceNumber))
        packet = self.__packetBuilder.build(packetType, sequenceNumber, content)
        self.__socketRC.sendto(packet.getBytes(), self.__routerAddr)

    def getPacket(self, timeout=None):
        self.__socketRC.settimeout(timeout)
       #TODO: decode pkt type and seq num

    def buildConnection(self):
        packet = self.getPacket()

        #boolean if connection is built
        #TODO: if pkt type is syn, send ack syn, if already acked, return true

        return False

    def getMessage(self):
        self.__socketRC = socket(AF_INET, SOCK_DGRAM)
        self.__socketRC.bind(('', self.__port))
        print("Listening")

        # Make sure we have some connection.
        if (self.buildConnection()):

            #TODO: if window not finished, keep doing till end, send ack pkt,

            return self.__window.getMessage()


