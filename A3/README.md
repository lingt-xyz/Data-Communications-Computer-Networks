### Tasks
1. UDP.
	1. There is no `accept` in UDP, it is connectionless.
	2. The `recvfrom` method returns not onloy the data but also the `host:port` of the sender. You should use the `received_addr` to reply.
	3. The `sendto` method requires two arguments: data to be sent, and the `host:port` of the receiver.
2. Addressing
	1. Use IPv4 addresses.
	2. Port number is represented by 2 bytes in Big-Endian order.
3. Automatic-Repeat-Request (ARQ) protocol: Selective Repeat ARQ/Selective Reject ARQ.
	1. Selective Repeat is part of the automatic repeat-request (ARQ). 
	2. With selective repeat, the sender sends a number of frames specified by a window size even without the need to wait for individual ACK from the receiver as in Go-Back-N ARQ.
	3. The receiver may selectively  reject  a  single  frame,  which  may  be  retransmitted  alone;  this  contrasts with  other  forms  of  ARQ,  which  must  send  every  frame  from  that  point  again.
	4. The  receiver  accepts  out-of-order frames and buffers them. The sender individually retransmits frames that have timed out.

4. Mimicking the TCP three-way handshaking.
5. Endianness
	1. Endianness is the order of bytes in a multiple-bytes representation such as word, integer, float. 
	2. When sending multi-bytes data type via a network, we must convert them from the host byte order to the network byte order (e.g., Big-Endian). 
	3. And when receiving multibytes data types from the network, we must convert them from the network byte order to the host order. 
	4. Most of the languages provide APIs for this conversion.
	
6. (optional) Support multiple clients at the server.

### Usage

### Grading Policy
1. With reliable environment: 6 Marks
	1. Three-way: 1 Mark
	2. GET: 2.5 Marks
	3. POST: 2.5 Marks
2. Drop: 1.5 Marks
3. Delay: 1.5 Marks
4. Both: 1 Marks
#### Optional Tasks (2 Marks)
1. Support Concurrent Requests: 1 Marks

### Test cases
