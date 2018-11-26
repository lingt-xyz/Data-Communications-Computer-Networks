import time
import threading
import math
from DealPackets.SelectiveRepeatWindow import *
from DealPackets.Packet import *
from const import *

#TODO: ? still think that should put Frame and window identities into SRW, inheritance
class Frame:
    def __init__(self, index, payload = None):
        self.index = index
        self.payload = payload
        self.send = False
        self.ACK = False
        self.timer = 0

class SenderWindow():
    def __init__(self, message):
        # number of packets
        self.numberOfFrames = math.ceil(len(message)/PAYLOAD_SIZE)
        # where the window starts from
        self.pointer = 0
        # init all packets
        for i in range(0, self.numberOfFrames):
            self.frames[i] = Frame(i+1, message[i * PAYLOAD_SIZE:(i + 1) * PAYLOAD_SIZE])

    def getFrames(self):
        """
        Get all sendable packets in WINDOW
        """
        frameList = []
        for i in range(self.pointer, self.pointer + WINDOW_SIZE):
            f = self.frames[i]
            if(not f.send):
                f.send = True
                frameList.append(f)
        return frameList

    def updateFrame(self, index):
        """
        When received an ACK, update WINDOW, slide WINDOW if necessary
        """
        self.frames[index].ACK = True
        offset = 0
        for i in range(self.pointer, self.pointer + WINDOW_SIZE):
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

    def process(self):
        #timer start
        timeis = time.time()

        #Check each window if frame is handled, if no or timed out, resend pkt
        for i in range(self.windowStart, self.windowSize):
            if (not self.frameHandled[i]):
                if (timeis > (DEFAULT_WAIT_TIME + self.frameTimer[i])):
                    self.sendPacket(PACKET_TYPE_DATA, i, self.frameData[i])

        # Wait for feedback.
        while (True):
            response = self.getResponse()

            if (response is not None):
                print("Response received")
                self.handleResponse(response)
            else:
                print("No response")
                break
            
        
        
    def handleResponse(self, packet):

        # Figure out what kind of packet it is.
        packetType = packet.packet_type


        if (packetType == PACKET_TYPE_AK):
            seq = packet.getSequenceNumber()

            for i in range(0, seq + 1):
                if i < self.windowSize:
                    if (not self.frameHandled[i]):
                        print("Got ak for " + str(i))
                        self.frameHandled[i] = True
                    else:
                        print("frame " + str(i) + " is already aked")
                else:
                    print("not in range")
        else:
            print(str(packetType))
