### Start
```
python3 httpc.py

python3 httpfs.py -v -p 8080

python3 httpfs.py -v -d data -p 8090

```

### File server
```
get 'http://localhost:8080/'
get -v 'http://localhost:8080/'
get -h Content-Type:application/json 'http://localhost:8080/'
get -h Content-Type:text/xml 'http://localhost:8080/'

get -v 'http://localhost:8080/foo'
get -h Content-Disposition:inline 'http://localhost:8080/filename'
get -v -h 'http://localhost:8080/../foo'
get -h Content-Disposition:inline 'http://localhost:8080/filename'

post -h Content-Type:application/json -d '{"": "somethingelse"}' http://localhost:8080/foo
```

### Content-Disposition:attachment 
```
http://localhost:8080/download
```

### Regular server
```
get 'http://localhost:8080/get'
get 'http://localhost:8080/get?user=a'
get 'http://localhost:8080/get?user=a&pwd=b'
post -v -h Content-Type:application/json -d '{"assignment": "3"}' http://localhost:8080/post
```
