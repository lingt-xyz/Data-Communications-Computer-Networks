import logging
from socket import *
from Transport.DealPackets.Packet import *
from Transport.DealPackets.packetConstructor import *
from Transport.Server.ServerWindow import *
from Transport.Client.ClientWindow import *
from Transport.const import *


class ReceiverController:
    address = None
    __conn = None
    __packetBuilder = None

    def __init__(self):
        self.__routerAddr = (ROUTER_IP,ROUTER_PORT)

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
                # send ACK
                p = self.__packetBuilder.build(PACKET_TYPE_AK)
                self.__conn.sendto(p.to_bytes(), self.__routerAddr)


    def sendMessage(self, message):
    	# Third, response
        window = ServerWindow(message)
            threading.Thread(target=self.receiveListener, args=(window)).start()
            while window.hasPendingPacket: # Not all packets have been sent
                # Get next sendable packets if there is any in WINDOW
                for frame in window.getFrames():
                    p = self.__packetBuilder.build(PACKET_TYPE_DATA, frame.index, frame.payload)
                    self.__conn.sendto(p.to_bytes(), self.__routerAddr)
                    frame.timer = time.time()
        # Fourth, Disconnect
        self.disConnect()

    def receiveListener(self, window):
        """
        Listen response from server
        """
        while window.hasPendingPacket:
            # Find packets that have been sent but have not been ACKed
            # Then, check their timer
            for i in range(self.pointer, self.pointer + WINDOW_SIZE):
                f = window.frames[i]
                if(f.send and not f.ACK):
                    if(f.timer + TIME_OUT > time.time()):
                        # reset send status, so it can be re-sent
                        f.send = False
            
            # update ACK
            response, sender = self.__conn.recvfrom(PACKET_SIZE) # TODO what if packet size is less than PACKET_SIZE?
            p = Packet.from_bytes(response)
            logging.debug('Payload: {}'.format(p.payload.decode("utf-8")))

            if(p.packet_type == PACKET_TYPE_AK):
                window.updateFrame([p.seq_num-1])

    def sendPacket(self, packetType, sequenceNumber, content=None):
        print("Sending packet type: " + str(packetType) + " with #" + str(sequenceNumber))
        packet = self.__packetBuilder.build(packetType, sequenceNumber, content)
        self.__conn.sendto(packet.getBytes(), self.__routerAddr)

    def getPacket(self, timeout=None):
        self.__conn.settimeout(timeout)
        try:
            data, addr = self.__conn.recvfrom(PACKET_SIZE)
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
        self.__conn = socket(AF_INET, SOCK_DGRAM)
        self.__conn.bind(('', SERVER_PORT))
        logging.info("Server is listening at {}:{}.".format(SERVER_IP, SERVER_PORT))

        packet = self.getPacket()

        # boolean if connection is built
        # if pkt type is syn, send ack syn, if already acked, return true
        if (packet.packet_type == PACKET_TYPE_SYN):
            addr = (packet.peer_ip_addr, packet.peer_port)
            self.sendPacket(PACKET_TYPE_SYN_AK, 0)
            # we can just ignore the comming ACK, because it could be lost but the sender would not deal with this case
            # but we do shuld be careful with the first packet when receiving the http request
            return True
        return False

    def disConnect(self):
        """
        Disconnecting: FIN, ACK, FIN, ACK
        """
        logging.info("Disconnecting from {}:{}.".format(self.__packetBuilder.__destinationAddress, self.__packetBuilder.destinationPort))
        self.__conn.close()


