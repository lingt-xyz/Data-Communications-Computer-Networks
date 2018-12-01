import logging
import time
import socket
from Packet import *
from packetConstructor import *
from const import *
from Window import *


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
        logging.info("Connecting to {}:{}.".format(SERVER_IP, SERVER_PORT))
        self.__routerAddr = (ROUTER_IP, ROUTER_PORT)
        peer_ip = ipaddress.ip_address(socket.gethostbyname(SERVER_IP))
        self.__packetBuilder = PacketConstructor(peer_ip, SERVER_PORT)
        self.__conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Send SYN
            p = self.__packetBuilder.build(PACKET_TYPE_SYN)
            self.__conn.sendto(p.to_bytes(), self.__routerAddr)
            self.__conn.settimeout(ALIVE)
            logging.debug('Waiting for a response')
            # Expecting SYN_ACK
            response, sender = self.__conn.recvfrom(PACKET_SIZE)
            p = Packet.from_bytes(response)
            logging.debug("Payload: {}".format(p.payload.decode("utf-8")))
            logging.info("Server connection established.")
        except socket.timeout:
            logging.err("No response after {}s".format(ALIVE))
            self.__conn.close()
            return False
        if p.packet_type == PACKET_TYPE_SYN_AK:
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
        # self.__routerAddr = (ROUTER_IP,ROUTER_PORT)
        self.__conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__conn.bind(('', SERVER_PORT))
        logging.info("Server is listening at {}:{}.".format(SERVER_IP, SERVER_PORT))

        packet = self.getPacket()
        # boolean if connection is built
        # if pkt type is syn, send ack syn, if already acked, return true
        if packet.packet_type == PACKET_TYPE_SYN:
            # addr = (packet.peer_ip_addr, packet.peer_port)
            packet.packet_type = PACKET_TYPE_SYN_AK
            self.__conn.sendto(packet.to_bytes(), self.__routerAddr)
            # we can just ignore the coming ACK, because it could be lost but the sender would not deal with this case
            # but we do should be careful with the first packet when receiving the http request
            logging.info("Client connection established.")
            return True
        return False

    def sendMessage(self, message):
        window = Window()
        window.createSenderWindow(message)

        threading.Thread(target=self.senderListener, args=(window,)).start()
        while window.hasPendingPacket:  # Not all packets have been sent
            # Get next sendable packets if there is any in WINDOW
            for frame in window.getFrames():
                p = self.__packetBuilder.build(PACKET_TYPE_DATA, frame.seq_num, frame.payload)
                self.__conn.sendto(p.to_bytes(), self.__routerAddr)
                print("--------------->Send: {}".format(p.payload))
                frame.timer = time.time()

    def senderListener(self, window):
        """
        Listen response from server
        """
        while window.hasPendingPacket:
            # Find packets that have been sent but have not been ACKed
            # Then, check their timer
            for i in range(window.pointer, window.pointer + WINDOW_SIZE):
                if i >= len(window.frames):
                    break
                f = window.frames[i]
                if f.send and not f.ACK:
                    if f.timer + TIME_OUT < time.time():
                        # reset send status, so it can be re-sent
                        f.send = False

            # update ACK
            response, sender = self.__conn.recvfrom(PACKET_SIZE)

            p = Packet.from_bytes(response)
            logging.debug('Payload: {}'.format(p.payload.decode("utf-8")))

            if p.packet_type == PACKET_TYPE_AK:
                window.updateWindow(p.seq_num)

    def receiveMessage(self):
        window = Window()
        window.createReceiverWindow()
        while not window.finished():
            # TODO if None, raise error
            p = self.getPacket()
            print("--------------->Received: {}".format(p.payload))
            # discard possible packet from handshake
            if p.packet_type == PACKET_TYPE_AK and p.seq_num == 0:
                continue
            window.process(p)
            # send ACK
            p.packet_type = PACKET_TYPE_AK
            self.__conn.sendto(p.to_bytes(), self.__routerAddr)

        data = self.retrieveData(window)
        return data

    # return data
    def retrieveData(self, window):
        data = b''
        for f in window.frames:
            data = data + f.payload
        return data.decode("utf-8")

    def getPacket(self):
        self.__conn.settimeout(ALIVE)
        try:
            data, addr = self.__conn.recvfrom(PACKET_SIZE)
            pkt = Packet.from_bytes(data)
            self.__routerAddr = addr

            if self.__packetBuilder is None:
                self.__packetBuilder = PacketConstructor(pkt.peer_ip_addr, pkt.peer_port)

            logging.debug("Got packet type: {} with #{}".format(str(pkt.packet_type), str(pkt.seq_num)))
            return pkt
        except socket.timeout:
            return None

    def disConnect(self):
        """
        Disconnecting: FIN, ACK, FIN, ACK
        """
        logging.info("Disconnecting.")
        self.__conn.close()
