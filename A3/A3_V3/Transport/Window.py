import time
import threading
import math
from Packet import *
from const import *

class Frame:
    def __init__(self, index, payload = None):
        # sequence number
        self.index = index
        # data
        self.payload = payload
        self.send = False
        self.ACK = False
        self.timer = 0

class Window():
    def __init__(self):
        # where WINDOW starts from
        self.pointer = 0
        # data
        self.frames = []

    def createSenderWindow(self, message):
        # number of packets
        self.numberOfPayload = math.ceil(len(message)/PAYLOAD_SIZE) 
        self.numberOfFrames = self.numberOfPayload + 1
        # init all packets
        for i in range(0, self.numberOfPayload):
            self.frames[i] = Frame(i+1, message[i * PAYLOAD_SIZE:(i + 1) * PAYLOAD_SIZE])
        self.frames[-1] = Frame(self.numberOfFrames-1, "###"+self.numberOfPayload+"###")

    def createReceiverWindow(self):
        pass

    def getFrames(self):
        """
        Get all sendable packets in WINDOW
        """
        frameList = []
        for i in range(self.pointer, self.pointer + WINDOW_SIZE):
            if(self.pointer + WINDOW_SIZE >= len(self.frames)):
                break
            f = self.frames[i]
            if(not f.send):
                f.send = True
                frameList.append(f)
        return frameList

    def updateWindow(self, index):
        """
        When received an ACK, update WINDOW, slide WINDOW if necessary
        """
        self.frames[index].ACK = True
        offset = 0
        for i in range(self.pointer, self.pointer + WINDOW_SIZE):
            if(self.pointer + WINDOW_SIZE >= len(self.frames)):
                break
            if(self.frames[i].ACK):
                offset+=1
            else:
                break
        self.pointer += offset

    def hasPendingPacket(self):
        """
        Check whether all packets have been ACKed
        """
        for i in range(0, self.numberOfFrames):
            if(not self.frames[i].ACK):
                return True
        return False

    def finished(self):
        # check payload ###total number###
        # if is last one, update fini
        p = self.frames[-1]
        pload = p.payload
        if ('#' in pload):
            pload = pload[3,-3]
            if(self.pointer == pload):
                self.fini = True

        return self.fini

    def process(self, p):
	# Is it in WINDOW range?
        index = p.seq_num - 1
        if self.pointer <= index < self.pointer + WINDOW_SIZE:
            # check whether already received
            if self.frames[index] is None:
                self.frames[index] = p
                self.updateWindow(p)
        else:
            # discard this packet
            pass

