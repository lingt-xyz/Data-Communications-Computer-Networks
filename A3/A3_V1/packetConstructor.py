from packet import Packet
import threading


class PacketConstructor:

    window_size = 10
    data_type = 0
    ack_type = 1
    syn_ack_type = 2
    syn_type = 3

    """
       Packet represents a simulated UDP packet.
    """

    def __init__(self):
        self.next_seq_num = 0
        self.received_packets = {}
        self.received_last_packet = False
        self.payload_lock = threading.Lock()

    def reset(self):
        self.payload = b''
        self.next_seq_num = 0
        self.received_packets = {}
        self.received_last_packet = False

    def received_all_packets(self):
        if not self.received_last_packet:
            return False
        next_seq_num = 0
        for seq_num in sorted(self.received_packets):
            if not seq_num == next_seq_num:
                return False
            next_seq_num += 1
        return True

    def assemble_payload(self):
        payload = b''
        for seq_num in sorted(self.received_packets):
            payload += self.received_packets[seq_num]
        return payload

    def send_ack(self, conn, seq_num, destination, peer_ip_addr, peer_port):
        p = Packet(packet_type=PacketConstructor.ack_type,
                   seq_num=seq_num,
                   peer_ip_addr=peer_ip_addr,
                   peer_port=peer_port,
                   is_last_packet=True,
                   payload=b'')
        print("sending ack " + str(seq_num))
        conn.sendto(p.to_bytes(), destination)

    def add_packet(self, p, conn, sender):
        if p.packet_type == PacketConstructor.data_type and p.seq_num >= self.next_seq_num and p.seq_num <= (
                self.next_seq_num + PacketConstructor.window_size):
            self.send_ack(conn, p.seq_num, sender, p.peer_ip_addr, p.peer_port)
            if p.seq_num not in self.received_packets:
                self.received_packets[p.seq_num] = p.payload
                while self.next_seq_num in self.received_packets:
                    self.next_seq_num += 1
                if (p.is_last_packet):
                    self.received_last_packet = True
                self.payload_lock.acquire()
                if (self.received_all_packets()):
                    payload = self.assemble_payload()
                    self.reset()
                    self.payload_lock.release()
                    return payload
                self.payload_lock.release()
            else:
                print("got out of order packet " + str(p.seq_num))
                # TODO: store the out of order packet somewhere
        else:
            print("got an out of window packet " + str(p.seq_num))
            # TODO: ?
        return None