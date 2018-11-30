from Transport.DealPackets.SelectiveRepeatWindow import *
from Transport.const import *
from Transport.Client.ClientWindow import Frame


class ServerWindow():

    def __init__(self):
        # where WINDOW starts from
        self.pointer = 0
        # WINDOW frames #TODO what's the size? Should use a list?
        self.numberOfFrames = 5
        self.frames = []
        self.fini = False

    def finished(self):
        return self.fini

    def process(self, p):
	# Is it in WINDOW range?
        index = p.seq_num - 1
        if self.pointer <= index < self.pointer + WINDOW_SIZE:
            # check whether already received
            if self.frames[index] is None:
                self.frames[index] = p
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
            self.fini = True
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
