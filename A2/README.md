### Tasks
1. Build your HTTP server library that implements the basic specifications.
2. Develop a minimal file server on top of the HTTP server library.
    1. GET / returns a list of the current files in the data directory. You can return different type format such as JSON, XML, plain text, HTML according to the Accept key of the header of the request. However, this is not mandatory; you can simply ignore the header value and make your server always returns the same output.
    2. GET /foo returns the content of the file named foo in the data directory. If the content does not exist, you should return an appropriate status code (e.g. HTTP ERROR 404).
    3. POST /bar should create or overwrite the file named bar in the data directory with the content of the body of the request. You can implement more options for the POST such as overwrite=true|false, but again this is optional.
3. Secure Access

    Your implementation may have a severe access vulnerability. The end-user could access not only the file of the default working directory of the server application but he/she could access most server files (read-write or read-only). To solve the previous problem, you should build a mechanism to prevent the clients to read/write any file outside the file server working directory.
4. Error Handling

    In this task, you need to enhance the file manager with the appropriate error handlers. In this context, each exception on the server side should be translated to an appropriate status code and human readable messages. For example, if the requested file does not exist, the file server should send a message with this information. Similarly, if the server is unable to process the request for security reasons ( the requested file is located outside the working directory), an appropriate handling must be performed.
5. (optional) Enhance the file server application to support simultaneous multi-requests.
    Your implementation of the file server may support only one client at given moments. Therefore, if you run multiple clients simultaneously, the server can answer only one request. To solve this problem, you are invited to develop a concurrent implementation of the file server, where the server can handle multiple requests simultaneously. The later means that you should have a dynamic data structure to scale according to the server machine capacity.
    
    To test your concurrent version, you can write a simple script to run multiple client instances (instances of httpc or curl). The script should take the number of client instances as a parameter. If you support concurrent requests, make sure the following scenarios work correctly:
    - Two clients are writing to the same file.
    - One client is reading, while another is writing to the same file.
    - Two clients are reading the same file.

6. (optional) Implement the support for Content-Type and Content-Disposition headers.
    Set appropriate values to the headers Content-Type and Content-Disposition headers for ‘GET /file’ requests. For more details, the you could consult 
    [5](https://www.w3.org/Protocols/rfc1341/4_Content-Type.html)
    [6](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition).

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
get 'http://localhost:8080/foo'
post -h Content-Type:application/json -d '{"": somecontent}' http://localhost:8080/filename

python3 httpfs.py -v -p 8090


```
