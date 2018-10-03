### Usage:

1. `python3 httpc.py get 'http://httpbin.org/get?course=networking&assignment=1'`
2. `python3 httpc.py get -v 'http://httpbin.org/get?course=networking&assignment=1'`
3. `python3 httpc.py -header --d post http://httpbin.org/post '{"Assignment": 1}' Content-Type:application/json`
4. `python3 httpc.py get 'http://google.ca/'`

### Redirection
* 301 Moved Permanently
  * Request
  ``` http
  GET /index.php HTTP/1.1
  Host: www.example.org
  ```
  * Response
  ``` http
  HTTP/1.1 301 Moved Permanently
  Location: http://www.example.org/index.asp
  ```
* 303 See Other
* 307 Temporary Redirect
* 308 Permanent Redirect
