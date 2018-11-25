import logging
from socket import *
from DealPackets.Packet import *
from Sender.SenderWindow import *
from DealPackets.packetConstructor import *
from const import *


class SenderController:
    __conn = None
    __routerAddr = None
    __packetBuilder = None

    def __init__(self):
        self.__routerAddr = (ROUTER_IP,ROUTER_PORT)
        self.__packetBuilder = PacketConstructor(SERVER_IP, SERVER_PORT)
    
    """
    The client invoke this function to send http request
    """
    def sendMessage(self, message):
        # first: connect
        if(self.connect()):
            # second: send message
            window = SenderWindow(message)
            while window.hasNext():
                payload = window.getNext()
                # ideally, we show throw this piece of code into a thread, so every frame can be handled correctly
                # threading.Thread(target=self.sendPacket, args=(conn, payload)).start()
                try:
                    p = self.__packetBuilder.build(PACKET_TYPE_DATA)
                    self.__conn.sendto(p.to_bytes(), self.__routerAddr)
                    self.__conn.settimeout(timeout)
                    logging.debug('Waiting for a response')
                    response, sender = self.__conn.recvfrom(1024)
                    p = Packet.from_bytes(response)
                    logging.debug('Payload: {}'.format(p.payload.decode("utf-8")))
                except socket.timeout:
                    logging.err('No response after {}s'.format(timeout))
                    # timeout: resend, but we need to reset the `send` status of the frame
                    # TODO: callback?
                
            # third: disconnect
            self.disConnect()
        else:
            logging.err("Cannot establish the connection to {}:{}.".format(SERVER_IP, SERVER_PORT))

    def sendPacket(self, payload):
        try:
            p = self.__packetBuilder.build(PACKET_TYPE_DATA)
            self.__conn.sendto(p.to_bytes(), self.__routerAddr)
            self.__conn.settimeout(timeout)
            logging.debug('Waiting for a response')
            response, sender = self.__conn.recvfrom(1024)
            p = Packet.from_bytes(response)
            logging.debug('Payload: {}'.format(p.payload.decode("utf-8")))
        except socket.timeout:
            logging.err('No response after {}s'.format(timeout))
            # timeout: resend, but we need to reset the `send` status of the frame
            # TODO: callback?
        
    def getResponse(self):
        try:
            data, addr = self.__socket.recvfrom(PACKET_SIZE)
            packet = Packet.from_bytes(data)
            print("Got packet type: " + str(packet.packet_type) + " with #" + str(packet.seq_num))
            return packet
        except Exception as e:
            print(e)
            return None

    """
    Three-way handshake
    """
    def connect(self):
        logging.info("Connecting to {}:{}.".format(SERVER_IP, SERVER_PORT))
        self.__conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        timeout = 5
        try:
            # send SYN
            p = self.__packetBuilder.build(PACKET_TYPE_SYN)
            self.__conn.sendto(p.to_bytes(), self.__routerAddr)
            self.__conn.settimeout(timeout)
            logging.debug('Waiting for a response')
            # expecting SYN_ACK
            response, sender = self.__conn.recvfrom(1024)
            p = Packet.from_bytes(response)
            logging.debug('Payload: {}'.format(p.payload.decode("utf-8")))
        except socket.timeout:
            logging.err('No response after {}s'.format(timeout))
            self.__conn.close()
            return False
        
        if(p.packet_type == PACKET_TYPE_SYN_AK):
            # send ACK
            p = self.__packetBuilder.build(PACKET_TYPE_AK)
            self.__conn.sendto(p.to_bytes(), self.__routerAddr)
            # no need to timeout, we know server is ready
            return True
        else:
            logging.err("Unexpected packet: {}".format(p.packet_type))
            self.__conn.close()
            return False
    
    """
    Disconnecting: FIN, ACK, FIN, ACK
    """
    def disConnect(self):
        # TODO disconnection
        logging.info("Disconnecting from {}:{}.".format(SERVER_IP, SERVER_PORT))
        self.__conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        timeout = 5
        try:
            p = self.__packetBuilder.build(PACKET_TYPE_NONE)
            self.__conn.sendto(p.to_bytes(), self.__routerAddr)
    
            # Try to receive a response within timeout
            self.__conn.settimeout(timeout)
            logging.debug('Waiting for a response')
            response, sender = self.__conn.recvfrom(1024)
            p = Packet.from_bytes(response)
            logging.debug('Payload: {}'.format(p.payload.decode("utf-8")))
        except socket.timeout:
            logging.err('No response after {}s'.format(timeout))
            self.__conn.close()
            return False
        
        if(p.packet_type == PACKET_TYPE_SYN_AK):
            p = self.__packetBuilder.build(PACKET_TYPE_AK)
            self.__conn.sendto(p.to_bytes(), self.__routerAddr)
            return True
        else:
            logging.err("Unexpected packet: {}".format(p.packet_type))
            self.__conn.close()
            return False
