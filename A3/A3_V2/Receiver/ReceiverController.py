from socket import *
from DealPackets.Packet import *
from DealPackets.packetConstructor import *
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

    def receiveMessage(self):
        """
        Receive message from the client
        """
        # First, connect
        # Second, receive request
        # Third, response
        # Fourth, Disconnect

    def sendPacket(self, packetType, sequenceNumber, content):
        print("Sending packet type: " + str(packetType) + " with #" + str(sequenceNumber))
        packet = self.__packetBuilder.build(packetType, sequenceNumber, content)
        self.__socketRC.sendto(packet.getBytes(), self.__routerAddr)

    def getPacket(self, timeout=None):
        self.__socketRC.settimeout(timeout)
        try:
            data, addr = self.__socketRC.recvfrom(PACKET_SIZE)
        except Exception as e:
            print(e)
            return None
        pkt = Packet.from_bytes(data)
        print("Got packet type: " + str(pkt.packet_type) + " with #" + str(pkt.seq_num))

        if (self.__packetBuilder is None):
            self.address = (pkt.getDestinationAddress(), pkt.getDestinationPort())
            self.__packetBuilder = PacketConstructor(pkt.getDestinationAddress(), pkt.getDestinationPort())

        return pkt

    def buildConnection(self):
        packet = self.getPacket()

        # boolean if connection is built
        # TODO: if pkt type is syn, send ack syn, if already acked, return true

        return False

    def getMessage(self):
        self.__socketRC = socket(AF_INET, SOCK_DGRAM)
        self.__socketRC.bind(('', self.__port))
        print("Listening")

        # Make sure we have some connection.
        if (self.buildConnection()):
            # TODO: if window not finished, keep doing till end, send ack pkt,

            return self.__window.getMessage()


