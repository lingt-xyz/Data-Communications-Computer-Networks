from DealPackets.SelectiveRepeatWindow import *
from DealPackets.packet import *


class SenderWindow(Window):
    def __init__(self, message, sendPacket, getResponse):
        '''''
        #TODO: windowSize=math.ceil(len(message)/payload)
        super().__init__(windowSize, sendPacket, getResponse)
        #0 - windowsize load msg into window
        '''''


    def process(self):
        #timer start


        # TODO: Check each window if frame is handled, if no or timed out, resend pkt


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
        packetType = packet.getPacketType();

        '''''
        if (packetType == AK): #TODO: pkt type 
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
        '''''
