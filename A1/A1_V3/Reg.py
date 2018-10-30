import re

def getHeaders(command):
    return re.findall('.* (-h (.*):(.*))* .*', command);
    #return command.split(" -h ")[1].split(" ")[0]

s1 = "httpc get -v -h key:value URL"
s2 = "httpc get -v -h key:value -h key1:value1 URL"

r = re.compile("-h (([\w-]+:[\w-]+))")
#print(r.findall(s1))
#print(r.findall(s2))
#print(re.findall("-h ([\w-]+:[\w-]+)", s2))
pairs = re.findall("-h ([\w-]+:[\w-]+)", s2)
#print("\r\n".join(pairs))

s3 = "post -h Content-Type:application/json -h ano12#:123D- http://httpbin.org/post"
pairs = re.findall("-h (.+?:.+?) ", s3)
print("\r\n".join(pairs))

m = re.match(r"/([\w_]+)\?", '/foo_123_?')
if(m):
	print(m.group(1))

m = re.match(r"/([\w_]+)\?", '/foo_123_')
if(m):
	print(m.group(1))
else:
	print("no match")

m = re.match(r"/([\w_]+)", '/foo_123_')
if(m):
	print(m.group(1))
else:
	print("no match")
