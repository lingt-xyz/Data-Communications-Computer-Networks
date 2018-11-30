import logging
from socket import *
from DealPackets.Packet import *
from DealPackets.packetConstructor import *
from Server.ServerWindow import *
import const


class ReceiverController:
    address = None
    __socketRC = None
    __packetBuilder = None

    def __init__(self):
        self.__routerAddr = (const.ROUTER_IP,const.ROUTER_PORT)

    def receiveMessage(self):
        """
        Receive message from the client
        """
        # First, connect

        if (self.buildConnection()):

            # Second, receive request
            window = ServerWindow()
            while not window.finished():
                p = self.getPacket()
                # TODO discard possible packet from handshake
                window.process(p)
                # TODO send ACK

            # Third, response

        # Fourth, Disconnect
        self.disConnect()

    def sendPacket(self, packetType, sequenceNumber, content=None):
        print("Sending packet type: " + str(packetType) + " with #" + str(sequenceNumber))
        packet = self.__packetBuilder.build(packetType, sequenceNumber, content)
        self.__socketRC.sendto(packet.getBytes(), self.__routerAddr)

    def getPacket(self, timeout=None):
        self.__socketRC.settimeout(timeout)
        try:
            data, addr = self.__socketRC.recvfrom(PACKET_SIZE)
        except socket.timeout:
            return None
        pkt = Packet.from_bytes(data)
        logging.debug("Got packet type: {} with #{}".format(str(pkt.packet_type),str(pkt.seq_num)))

        if (self.__packetBuilder is None):
            self.address = (pkt.getDestinationAddress(), pkt.getDestinationPort())
            self.__packetBuilder = PacketConstructor(pkt.getDestinationAddress(), pkt.getDestinationPort())

        return pkt

    def buildConnection(self):
	"""
	Three-way handshake
	"""
        self.__socketRC = socket(AF_INET, SOCK_DGRAM)
        self.__socketRC.bind(('', const.SERVER_PORT))
        logging.info("Server is listening at {}:{}.".format(const.SERVER_IP, const.SERVER_PORT))

        packet = self.getPacket()

        # boolean if connection is built
        # TODO: if pkt type is syn, send ack syn, if already acked, return true
        if (packet.packet_type == PACKET_TYPE_SYN):
            addr = (packet.peer_ip_addr, packet.peer_port)
            self.sendPacket(PACKET_TYPE_SYN_AK, 0)
            # we can just ignore the comming ACK, because it could be lost but the sender would not deal with this case
            # but we do shuld be careful with the first packet when receiving the http request
            return True
    '''''
            packet = self.getPacket()

            if (packet.packet_type == PACKET_TYPE_AK):
                windowSize = int(packet.payload.rstrip())
                self.__window = ReceiverWindow(windowSize, self.sendPacket, self.getPacket)
                return True
    '''''
        return False

    def disConnect(self):
        """
        Disconnecting: FIN, ACK, FIN, ACK
        """
        logging.info("Disconnecting from {}:{}.".format(self.__packetBuilder.__destinationAddress, self.__packetBuilder.destinationPort))
        self.__conn.close()

    '''''
    def getMessage(self):
        self.__socketRC = socket(AF_INET, SOCK_DGRAM)
        self.__socketRC.bind(('', self.__port))
        print("Listening")

        # Make sure we have some connection.
        if (self.buildConnection()):
            # TODO: if window not finished, keep doing till end, send ack pkt,

            return self.__window.getMessage()
    '''''

