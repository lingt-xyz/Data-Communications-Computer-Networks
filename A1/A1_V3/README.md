### Usage:

1. `python3 httpc.py`
2. Follow the prompt, input one of the followings
    1. `get 'http://httpbin.org/get?course=networking&assignment=1'`
    2. `get -v 'http://httpbin.org/get?course=networking&assignment=1'`
    3. `post -h Content-Type:application/json -d '{"Assignment": "1"}' http://httpbin.org/post`
    4. `post -v -h Content-Type:application/json -d '{"Assignment": 1}' http://httpbin.org/post`
    5. `get -v 'http://httpbin.org/get?course=networking&assignment=1' -o hello.txt`
    6. `get 'http://google.ca/'`
    7. `get -v 'http://google.ca/'`
    8. `post -h Content-Type:application/json -f test.txt http://httpbin.org/post`
    9. `post -h Content-Type: file/txt -f test.txt http://httpbin.org/post -o filewrite.txt`
    9. `post -h Content-Type:application/json -h hk1:hv1 -d '{"Assignment": 1}' http://httpbin.org/post`
