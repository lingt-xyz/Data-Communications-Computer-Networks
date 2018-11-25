from DealPackets.Packet import *

class PacketConstructor:
        __destinationAddress = None
        __destinationPort = None

        def __init__(self, destinationAddress, destinationPort):
                self.__destinationAddress = destinationAddress
                self.__destinationPort = destinationPort

        def build(self, packetType, sequenceNumber = 0, payload = None):
                return Packet(packetType, sequenceNumber, self.__destinationAddress, self.__destinationPort, payload)
