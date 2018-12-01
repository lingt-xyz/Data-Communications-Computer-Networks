import time
import threading
import math
from Packet import *
from const import *
import logging


class Frame:
    def __init__(self, seq_num, payload=None, is_last=False):
        # sequence number
        self.seq_num = seq_num
        # data
        self.payload = payload
        self.is_last = is_last
        self.send = False
        self.ACK = False
        self.timer = 0


class Window:
    def __init__(self):
        # where WINDOW starts from
        self.pointer = 0
        # data
        self.frames = []
        self.numberOfPayload = 0
        self.fini = False

    def createSenderWindow(self, message):
        # number of packets
        self.numberOfPayload = math.ceil(len(message)/PAYLOAD_SIZE) 
        # init all packets
        for i in range(0, self.numberOfPayload):
            if i == self.numberOfPayload - 1:
                self.frames.append(Frame(i + 1, message[i * PAYLOAD_SIZE:], True))
            else:
                self.frames.append(Frame(i + 1, message[i * PAYLOAD_SIZE:(i + 1) * PAYLOAD_SIZE]))

    def createReceiverWindow(self):
        pass

    def getFrames(self):
        """
        Get all sendable packets in WINDOW
        """
        frameList = []
        for i in range(self.pointer, self.pointer + WINDOW_SIZE):
            if i >= len(self.frames):
                break
            f = self.frames[i]
            if not f.send:
                f.send = True
                frameList.append(f)
        return frameList

    def updateWindow(self, seq_num):
        """
        When received an ACK, update WINDOW, slide WINDOW if necessary
        """
        self.frames[seq_num - 1].ACK = True
        offset = 0
        for i in range(self.pointer, self.pointer + WINDOW_SIZE):
            if i >= len(self.frames):
                break
            if self.frames[i].ACK:
                offset += 1
            else:
                break
        self.pointer += offset

    def hasPendingPacket(self):
        """
        Check whether all packets have been ACKed
        """
        logging.debug("---------------->Number of frames: {}".format(self.numberOfFrames))
        for i in range(0, self.numberOfFrames):
            logging.debug("---------------->Check frames: {}".format(self.frames[i].ACK))

        for i in range(0, self.numberOfFrames):
            if not self.frames[i].ACK:
                return True
        return False

    def finished(self):
        # check payload ###total number###
        # if is last one, update fini
        if self.frames:
            f = self.frames[-1]
            if f.is_last:
                if self.pointer == len(self.frames):
                    self.fini = True

        return self.fini

    def process(self, p):
        # Is it in WINDOW range?
        index = p.seq_num - 1
        if self.pointer <= index < self.pointer + WINDOW_SIZE:
            # check whether already received
            while index >= len(self.frames):
                self.frames.append(None)
            if self.frames[index] is None:
                self.frames[index] = Frame(index, p.payload, True)
                self.updateWindow(index)
        else:
            # discard this packet
            pass

