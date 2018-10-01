Usage:

1. python3 httpc.py get 'http://httpbin.org/get?course=networking&assignment=1'
2. python3 httpc.py get -v 'http://httpbin.org/get?course=networking&assignment=1'
3. python3 httpc.py -header --d post http://httpbin.org/post '{"Assignment": 1}' Content-Type:application/json
