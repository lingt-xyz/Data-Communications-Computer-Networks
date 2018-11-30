import logging
import time
from socket import *
from Transport.Packet import *
from Transport.packetConstructor import *
from Transport.const import *


class ClientController:
    __conn = None
    __routerAddr = None
    __packetBuilder = None

    def __init__(self):
        self.__routerAddr = (ROUTER_IP,ROUTER_PORT)
        self.__packetBuilder = PacketConstructor(SERVER_IP, SERVER_PORT)

    def connectServer(self):
        """
        Three-way handshake
        """
        logging.info("Connecting to {}:{}.".format(SERVER_IP, SERVER_PORT))
        self.__routerAddr = (ROUTER_IP,ROUTER_PORT)
        self.__packetBuilder = PacketConstructor(SERVER_IP, SERVER_PORT)
        self.__conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Send SYN
            p = self.__packetBuilder.build(PACKET_TYPE_SYN)
            self.__conn.sendto(p.to_bytes(), self.__routerAddr)
            self.__conn.settimeout(TIME_OUT)
            logging.debug('Waiting for a response')
            # Expecting SYN_ACK
            response, sender = self.__conn.recvfrom(PACKET_SIZE)
            p = Packet.from_bytes(response)
            logging.debug('Payload: {}'.format(p.payload.decode("utf-8")))
        except socket.timeout:
            logging.err('No response after {}s'.format(timeout))
            self.__conn.close()
            return False
        if(p.packet_type == PACKET_TYPE_SYN_AK):
            # Send ACK
            p = self.__packetBuilder.build(PACKET_TYPE_AK)
            self.__conn.sendto(p.to_bytes(), self.__routerAddr)
            # No need to timeout, we know server is ready
            return True
        else:
            logging.err("Unexpected packet: {}".format(p.packet_type))
            self.__conn.close()
            return False

    def connectClient(self):
	"""
	Three-way handshake
	"""
        self.__routerAddr = (ROUTER_IP,ROUTER_PORT)
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

    def sendMessage(self, message):
	    window = Window(message)
	    threading.Thread(target=self.senderListener, args=(window)).start()
	    while window.hasPendingPacket: # Not all packets have been sent
		# Get next sendable packets if there is any in WINDOW
		for frame in window.getFrames():
		    p = self.__packetBuilder.build(PACKET_TYPE_DATA, frame.index, frame.payload)
		    self.__conn.sendto(p.to_bytes(), self.__routerAddr)
		    frame.timer = time.time()

    def senderListener(self, window):
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
                window.updateWindow([p.seq_num-1])

    def receiveMessage(self):
	window = Window()
            while not window.finished():
                p = self.getPacket()
                # TODO discard possible packet from handshake
                window.process(p)
                # send ACK
                p = self.__packetBuilder.build(PACKET_TYPE_AK)
                self.__conn.sendto(p.to_bytes(), self.__routerAddr)
          #TODO return data  

    def getPacket(self):
        self.__conn.settimeout(ALIVE)
        try:
            data, addr = self.__conn.recvfrom(PACKET_SIZE)
            pkt = Packet.from_bytes(data)
            if (self.__packetBuilder is None):
                self.address = (pkt.getDestinationAddress(), pkt.getDestinationPort())
                self.__packetBuilder = PacketConstructor(pkt.getDestinationAddress(), pkt.getDestinationPort())
            logging.debug("Got packet type: {} with #{}".format(str(pkt.packet_type),str(pkt.seq_num)))
            return pkt
        except socket.timeout:
            return None

    
    def disConnect(self):
        """
        Disconnecting: FIN, ACK, FIN, ACK
        """
        logging.info("Disconnecting.")
        self.__conn.close()
