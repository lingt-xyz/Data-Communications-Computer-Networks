import logging
import time
import socket
from Packet import *
from packetConstructor import *
from const import *
from Window import *
import sys


class UdpController:
    __conn = None
    __routerAddr = None
    __packetBuilder = None

    def __init__(self):
        pass

    def connectServer(self):
        """
        Three-way handshake
        """
        logging.info("[Transport] Connecting to {}:{}.".format(SERVER_IP, SERVER_PORT))
        self.__routerAddr = (ROUTER_IP, ROUTER_PORT)
        peer_ip = ipaddress.ip_address(socket.gethostbyname(SERVER_IP))
        self.__packetBuilder = PacketConstructor(peer_ip, SERVER_PORT)
        self.__conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Send SYN
            p = self.__packetBuilder.build(PACKET_TYPE_SYN)
            self.__conn.sendto(p.to_bytes(), self.__routerAddr)
            self.__conn.settimeout(ALIVE)
            logging.debug('[Transport] Client Waiting for a response from the server.')
            # Expecting SYN_ACK
            response, sender = self.__conn.recvfrom(PACKET_SIZE)
            p = Packet.from_bytes(response)
            logging.info("[Transport] Server connection established.")
        except socket.timeout:
            print("[Transport] Connecting timeout.")
            self.__conn.close()
            sys.exit(0)
        if p.packet_type == PACKET_TYPE_SYN_AK:
            # Send ACK
            p = self.__packetBuilder.build(PACKET_TYPE_AK)
            self.__conn.sendto(p.to_bytes(), self.__routerAddr)
            # No need to timeout, we know server is ready
            return True
        else:
            print("[Transport] Unexpected packet: {}".format(p))
            self.__conn.close()
            sys.exit(0)

    def connectClient(self):
        """
        Three-way handshake
        """
        # self.__routerAddr = (ROUTER_IP,ROUTER_PORT)
        self.__conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__conn.bind(('', SERVER_PORT))
        logging.info("[Transport] Server is listening at {}:{}.".format(SERVER_IP, SERVER_PORT))

        packet = self.getPacket(ALIVE)
        if packet is None:
            print("[Transport] Connecting timeout.")
            # TODO confirm timeout
            return False
        # if pkt type is syn, send ack syn, if already acked, return true
        if packet.packet_type == PACKET_TYPE_SYN:
            # addr = (packet.peer_ip_addr, packet.peer_port)
            packet.packet_type = PACKET_TYPE_SYN_AK
            self.__conn.sendto(packet.to_bytes(), self.__routerAddr)
            # we can just ignore the coming ACK, because it could be lost but the sender would not deal with this case
            # but we do should be careful with the first packet when receiving the http request
            logging.info("[Transport] Client connection established.")
            return True
        return False

    def sendMessage(self, message):
        window = Window()
        window.createSenderWindow(message)

        threading.Thread(target=self.senderListener, args=(window,)).start()
        while window.hasPendingPacket():  # Not all packets have been sent
            # Get next sendable packets if there is any in WINDOW
            for frame in window.getFrames():
                p = self.__packetBuilder.build(PACKET_TYPE_DATA, frame.seq_num, frame.payload)
                self.__conn.sendto(p.to_bytes(), self.__routerAddr)
                logging.debug("[Transport] Send Message: {}".format(p.payload))
                frame.timer = time.time()
                frame.send = True

    def senderListener(self, window):
        """
        Listen response from server
        """
        while window.hasPendingPacket():
            # Find packets that have been sent but have not been ACKed
            # Then, check their timer
            try:
                self.__conn.settimeout(TIME_OUT)
                response, sender = self.__conn.recvfrom(PACKET_SIZE)
                p = Packet.from_bytes(response)
                logging.debug('[Transport] Received response: {}: {}'.format(p, p.payload.decode("utf-8")))
                if p.packet_type == PACKET_TYPE_AK:
                    window.updateWindow(p.seq_num)
            except socket.timeout:
                logging.debug("[Transport] Timeout when wait ACK.")
                for i in range(window.pointer, window.pointer + WINDOW_SIZE):
                    if i >= len(window.frames):
                        break
                    f = window.frames[i]
                    if f.send and not f.ACK:
                        # reset send status, so it can be re-sent
                        f.send = False

        logging.debug('[Transport] Listener reaches the end!')

    def receiveMessage(self):
        window = Window()
        window.createReceiverWindow()
        while not window.finished():
            # TODO if None, raise error
            p = self.getPacket(TIME_OUT_FOR_RECEIVE)
            if p is None:
                logging.debug("[Transport] No message received in timeout time")
                return None
            # discard possible packet from handshake
            if p.packet_type == PACKET_TYPE_AK and p.seq_num == 0:
                continue
            window.process(p)
            # send ACK
            p.packet_type = PACKET_TYPE_AK
            self.__conn.sendto(p.to_bytes(), self.__routerAddr)

        data = self.retrieveData(window)
        return data

    # return data (bytes)
    def retrieveData(self, window):
        data = b''
        for f in window.frames:
            data = data + f.payload
        return data

    def getPacket(self, timeout):
        self.__conn.settimeout(timeout)
        try:
            data, addr = self.__conn.recvfrom(PACKET_SIZE)
            pkt = Packet.from_bytes(data)
            logging.debug("[Transport] Received: {}:{}".format(pkt,pkt.payload))
            self.__routerAddr = addr

            if self.__packetBuilder is None:
                self.__packetBuilder = PacketConstructor(pkt.peer_ip_addr, pkt.peer_port)

            return pkt
        except socket.timeout:
            logging.debug('[Transport] Time out when recvfrom message!')
            return None

    def dis_connect(self):
        """
        Disconnecting: FIN, ACK, FIN, ACK
        """
        logging.info("Disconnecting.")
        self.__conn.close()
