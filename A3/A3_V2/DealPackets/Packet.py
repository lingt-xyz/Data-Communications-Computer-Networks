import ipaddress

MIN_LEN = 11
MAX_LEN = 1024

PACKET_TYPE_NONE = 0
PACKET_TYPE_DATA = 1
PACKET_TYPE_SYN = 2
PACKET_TYPE_SYN_AK = 3
PACKET_TYPE_AK = 4

PACKET_TYPE_SIZE = 1
SEQUENCE_SIZE = 4
DESTINATION_ADDRESS_SIZE = 4
DESTINATION_PORT_SIZE = 2
PAYLOAD_SIZE = 1013
PACKET_SIZE = PACKET_TYPE_SIZE + SEQUENCE_SIZE + DESTINATION_ADDRESS_SIZE + DESTINATION_PORT_SIZE + PAYLOAD_SIZE



class Packet:

    """
    Packet represents a simulated UDP packet.
    """

    def __init__(self, packet_type, seq_num, peer_ip_addr, peer_port, is_last_packet, payload):
        self.packet_type = int(packet_type)
        self.seq_num = int(seq_num)
        self.peer_ip_addr = peer_ip_addr
        self.peer_port = int(peer_port)
        self.is_last_packet = is_last_packet
        self.payload = payload

    def to_bytes(self):
        """
        to_raw returns a bytearray representation of the packet in big-endian order.
        """
        buf = bytearray()
        buf.extend(self.packet_type.to_bytes(1, byteorder='big'))
        buf.extend(self.seq_num.to_bytes(4, byteorder='big'))
        buf.extend(self.peer_ip_addr.packed)
        buf.extend(self.peer_port.to_bytes(2, byteorder='big'))
        last_packet = 0
        if self.is_last_packet:
            last_packet = 1
        buf.extend(last_packet.to_bytes(1, byteorder='big'))

        buf.extend(self.payload)

        return buf

    def __repr__(self, *args, **kwargs):
        return "#%d, peer=%s:%s, size=%d" % (self.seq_num, self.peer_ip_addr, self.peer_port, len(self.payload))

    @staticmethod
    def from_bytes(raw):
        """from_bytes creates a packet from the given raw buffer.

            Args:
                raw: a bytearray that is the raw-representation of the packet in big-endian order.

            Returns:
                a packet from the given raw bytes.

            Raises:
                ValueError: if packet is too short or too long or invalid peer address.
        """
        if len(raw) < Packet.MIN_LEN:
            raise ValueError("packet is too short: {} bytes".format(len(raw)))
        if len(raw) > Packet.MAX_LEN:
            raise ValueError("packet is exceeded max length: {} bytes".format(len(raw)))

        curr = [0, 0]

        def nbytes(n):
            curr[0], curr[1] = curr[1], curr[1] + n
            return raw[curr[0]: curr[1]]

        packet_type = int.from_bytes(nbytes(1), byteorder='big')
        seq_num = int.from_bytes(nbytes(4), byteorder='big')
        peer_addr = ipaddress.ip_address(nbytes(4))
        peer_port = int.from_bytes(nbytes(2), byteorder='big')
        last_packet = int.from_bytes(nbytes(1), byteorder='big')
        is_last_packet = (last_packet == 1)
        payload = raw[curr[1]:]

        return Packet(packet_type=packet_type,
                      seq_num=seq_num,
                      peer_ip_addr=peer_addr,
                      peer_port=peer_port,
                      is_last_packet=is_last_packet,
                      payload=payload)
