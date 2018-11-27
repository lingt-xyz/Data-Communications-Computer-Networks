import logging
import time
from socket import *
from DealPackets.Packet import *
from DealPackets.packetConstructor import *
from Client.ClientWindow import *
from DealPackets.SelectiveRepeatWindow import *
from const import *


class ClientController:
    __conn = None
    __routerAddr = None
    __packetBuilder = None

    def __init__(self):
        self.__routerAddr = (ROUTER_IP,ROUTER_PORT)
        self.__packetBuilder = PacketConstructor(SERVER_IP, SERVER_PORT)
    
    def sendMessage(self, message):
        """
        The client invoke this function to send http request
        """
        # First: connect
        if(self.connect()):
            # Second: send message
            window = SenderWindow(message)
            threading.Thread(target=self.receiveListener, args=(window)).start()
            while window.hasPendingPacket: # Not all packets have been sent
                # Get next sendable packets if there is any in WINDOW
                for frame in window.getFrames():
                    p = self.__packetBuilder.build(PACKET_TYPE_DATA, frame.index, frame.payload)
                    self.__conn.sendto(p.to_bytes(), self.__routerAddr)
                    frame.timer = time.time()
        else:
            logging.err("Cannot establish the connection to {}:{}.".format(SERVER_IP, SERVER_PORT))
    
    def getReponse(self):
        """
        The client invoke this function to get http response
        """
        # First: connect
        if(self.connect()):
            # Second: send message
            window = SenderWindow(message)
            # Third: start a thread to receive responses
            threading.Thread(target=self.receiveListener, args=(window)).start()
            while window.hasPendingPacket: # Not all packets have been sent
                # Get next sendable packets if there is any in WINDOW
                for frame in window.getFrames():
                    p = self.__packetBuilder.build(PACKET_TYPE_DATA, frame.index, frame.payload)
                    self.__conn.sendto(p.to_bytes(), self.__routerAddr)
                    frame.timer = time.time()
                    
            # Third: disconnect
            self.disConnect()
        else:
            logging.err("Cannot establish the connection to {}:{}.".format(SERVER_IP, SERVER_PORT))


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

    def connect(self):
        """
        Three-way handshake
        """
        logging.info("Connecting to {}:{}.".format(SERVER_IP, SERVER_PORT))
        self.__conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        timeout = 5
        try:
            # Send SYN
            p = self.__packetBuilder.build(PACKET_TYPE_SYN)
            self.__conn.sendto(p.to_bytes(), self.__routerAddr)
            self.__conn.settimeout(timeout)
            logging.debug('Waiting for a response')
            # Expecting SYN_ACK
            response, sender = self.__conn.recvfrom(1024)
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
    
    def disConnect(self):
        """
        Disconnecting: FIN, ACK, FIN, ACK
        """
        logging.info("Disconnecting from {}:{}.".format(SERVER_IP, SERVER_PORT))
        self.__conn.close()
