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
        try:
            data, addr = self.__socket.recvfrom(PACKET_SIZE)
            packet = Packet.from_bytes(data)
            print("Got packet type: " + str(packet.packet_type) + " with #" + str(packet.seq_num))
            return packet
        except Exception as e:
            print(e)
            return None

    def connect(self, windowSize):

        for i in range(0, 5):
            print("Trying to connect: " + str(i))
            self.sendPacket(PACKET_TYPE_SYN, 0, "")
            response = self.getResponse()

            if (response is not None and response.packet_type == PACKET_TYPE_SYN_AK):
                self.sendPacket(PACKET_TYPE_AK, 0, str(windowSize))
                return True

        return False

    def getSocketPort(self):
        return self.__port
