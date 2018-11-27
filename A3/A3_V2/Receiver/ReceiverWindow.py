from DealPackets.SelectiveRepeatWindow import *


class ReceiverWindow():

    def __init__(self):
        # where WINDOW starts from
        self.pointer = 0
        # WINDOW frames #TODO what's the size? Should use a list?
        self.frames = []

    def finished(self):
        for i in range(0, self.windowSize):
            if not self.frameHandled[i]:
                return False

        return True

    def process(self, p):
	# Is it in WINDOW range?
        index = p.seq_num - 1
        if self.pointer <= index < self.pointer + WINDOW_SIZE
            # check whether already received
            if self.frames[index] is None:
                self.frames[inex] = p
                # Should slide? Is it last one?
                self.updateWindow(p)
        else:
            # discard this packet
            pass

    def updateWindow(self,p):
	"""
	If the packet is the last one, set Finished status
	Else, update WINDOW
	"""
	# TODO check is it last packet?
	last = False
	if last:
	else:
	for i in range(self.pointer, self.pointer + WINDOW_SIZE):
            # TODO check indexOutOfBoundException
            if(self.frames[i] is not None):
                offset+=1
            else:
                break
        self.pointer += offset

    def handleResponse(self, packet):

        if (packet.packet_type == PACKET_TYPE_DATA):
            seq = packet.seq_num

            self.frameData[seq] = packet.payload
            self.frameHandled[seq] = True
