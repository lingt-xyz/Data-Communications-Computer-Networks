from DealPackets.SelectiveRepeatWindow import *


class ReceiverWindow(Window):

    def __init__(self, windowSize, sendPacket, getResponse):
        super().__init__(windowSize, sendPacket, getResponse)

    def finished(self):
        for i in range(0, self.windowSize):
            if not self.frameHandled[i]:
                return False

        return True

    def process(self):
        #timer
        timeis = time.time()

        #Check each window if frame is handled or timed out
        for i in range(self.windowStart, self.windowSize):
            if (not self.frameHandled[i]):
                if (timeis > (DEFAULT_WAIT_TIME + self.frameTimer[i])):
                    self.sendPacket(PACKET_TYPE_AK, i - 1, "")

                break


        # Wait for incoming data
        while (True):
            response = self.getResponse(1)

            if (response is not None):
                self.handleResponse(response)
            else:
                print("No response")
                break

    def handleResponse(self, packet):

        if (packet.packet_type == PACKET_TYPE_DATA):
            seq = packet.getSequenceNumber()

            self.frameData[seq] = packet.payload
            self.frameHandled[seq] = True
