from Method import Method

key = None
value = None
url = None
data = None
file_content = None
rfname = None
newurl = None


def command_pro(cmd):
    if ("help" in cmd):

        showhelpmenu()

    elif ("get" in cmd):

        if ("-h" not in cmd):

            method.http_get(cmd, None, None, None)

        elif ("-h" in cmd):

            setkv(cmd)
            method.http_get(cmd, key, value, None)



    elif ("redirect" in cmd):

        seturl(cmd)
        method_r.redirect()
        global newurl
        newurl = method_r.getnewurl()
        print(newurl)

        m = Method(newurl)
        m.http_get(cmd, None, None, None)

    elif ("post" in cmd):

        setkv(cmd)
        if ("-d" in cmd and "-f" not in cmd):
            setdata(cmd)
            method_.http_post(cmd, key, value, data, None)
        if ("-f" in cmd and "-d" not in cmd):
            setfile(cmd)
            method_.http_post(cmd, key, value, file_content, None)


    else:
        print("Invalid command")


def file_pro(cmd):
    if ("help" in cmd):
        showhelpmenu()

    if ("get" in cmd):

        if ("-h" not in cmd):

            method.http_get(cmd, None, None, rfname)

        elif ("-h" in cmd):

            setkv(cmd)
            method.http_get(cmd, key, value, rfname)



    elif ("post" in cmd):

        setkv(cmd)
        if ("-d" in cmd and "-f" not in cmd):
            setdata(cmd)
            method_.http_post(cmd, key, value, data, rfname)
        if ("-f" in cmd and "-d" not in cmd):
            setfile(cmd)
            method_.http_post(cmd, key, value, file_content, rfname)


def setkv(c):
    key_pos = c.find("-h") + 3
    colon_pos = c.find(":") + 1
    value_pos = c.find(":") + 2
    http_pos = c.find("http")
    data_pos = c.find("-d") - 1
    data_pos_ = c.find("-f") - 1
    global key
    global value
    key = c[key_pos:colon_pos]
    if ("post" in c):
        if ("-d" in c):
            value = c[value_pos:data_pos]
        elif ("-f" in c):
            value = c[value_pos:data_pos_]
    elif ("get" in c):
        value = c[value_pos:http_pos]


def seturl(c):
    global url
    url_pos = c.find("http")
    url = c[url_pos:]
    if ("-o" in c):
        o_pos = c.find("-o") - 1
        url = c[url_pos:o_pos]


def setdata(c):
    global data
    data_pos = c.find("-d") + 3
    url_pos = c.find("http") - 1
    data = c[data_pos:url_pos]


def setfile(c):
    global file_content
    file_pos = c.find("-f") + 4
    url_pos = c.find("http") - 2
    file_name = c[file_pos:url_pos]

    with open(file_name, 'r') as f:
        file_content = f.read()


def findrfname(c):
    global rfname
    rfname_pos = c.find("-o") + 2
    rfname = c[rfname_pos:]


def showhelpmenu():
    print("httpc is a curl-like application but supports HTTP protocol only." + "\n" +
          "Usage: " + "\n" +
          "httpc command [arguments]" + "\n" +
          "The commands are: " + "\n" +
          "get    executes a HTTP GET request and prints the response." + "\n" +
          "post   executes a HTTP POST request and prints the resonse." + "\n" +
          "help   prints this screen." + "\n")


control = True
while control:

    cmd_ = input("please enter the command" + "\n" + "httpc ")
    seturl(cmd_)

    if ("help" not in cmd_):
        method = Method(url)
        method_ = Method(url)
        method_r = Method(url)

    if ("-o" not in cmd_):
        command_pro(cmd_)
    else:
        findrfname(cmd_)
        file_pro(cmd_)

    ans = input("Continue?" + "\n")

    if ans == "yes":
        control = True
    else:
        control = False


