### Tasks
1. UDP.
2. Automatic-Repeat-Request (ARQ) protocol: Selective Repeat ARQ/Selective Reject ARQ.
	
	Selective Repeat is part of the automatic repeat-request (ARQ). With selective repeat, the sender sends a number of frames specified by a window size even without the need to wait for individual ACK from the receiver as in Go-Back-N ARQ. The receiver may selectively  reject  a  single  frame,  which  may  be  retransmitted  alone;  this  contrasts with  other  forms  of  ARQ,  which  must  send  every  frame  from  that  point  again.  The  receiver  accepts  out-of-order frames and buffers them. The sender individually retransmits frames that have timed out.

3. Mimicking the TCP three-way handshaking.

4. (optional) Support multiple clients at the server.

### Usage
httpfs is a simple file server.
usage: `httpfs [-v] [-p PORT] [-d PATH-TO-DIR]`

* `-v` Prints debugging messages.
* `-p` Specifies the port number that the server will listen and serve at Default is 8080.
* `-d` Specifies the directory that the server will use to read/write requested files. Default is the current directory when launching the application.

### Grading Policy
1. Implement HTTP server library: 3 Marks
2. Implement GET /: 2 Marks
3. Implement GET /filename: 2 Marks
4. Implement POST /filename: 2 Marks
5. Security Hardening: 0.5 Marks
6. Error handling: 0.5 Marks
#### Optional Tasks (2 Marks)
1. Support Concurrent Requests: 1 Marks
2. Support Content-Type and Content-Disposition: 1 Marks

### Test cases
```
python3 httpc.py
get 'http://localhost:8080/'
get -v 'http://localhost:8080/'
get -h Content-Type:application/json 'http://localhost:8080/'
get -h Content-Type:text/xml 'http://localhost:8080/'

get -v 'http://localhost:8080/foo'
get -h Content-Disposition:inline 'http://localhost:8080/filename'
get -v -h Content-Disposition:inline 'http://localhost:8080/../foo'
get -h Content-Disposition:inline 'http://localhost:8080/filename'


post -h Content-Type:application/json -d '{"": "somethingelse"}' http://localhost:8080/foo

python3 httpfs.py -v -p 8080

python3 httpfs.py -v -d data -p 8090


```
