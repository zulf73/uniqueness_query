import http.server
import socketserver
import time
import BaseHTTPServer
from urlparse import urlparse, parse_qs
import json
from pymongo import MongoClient
import sys

def count(uri,dbname,colname, query):
    client = MongoClient(uri)
    coll = client[dbname][colname]
    return coll.find_one(query)


def uniqueness_query(counter):
    a = 'mongodb+srv://unique:unique@cluster0-3cmqe.mongodb.net/prod?retryWrites=true&w=majority'
    b = 'uniqueness'
    c = counter
    z = count(a,'prod',b, { 'counter': int(c)})
    ans = '{ '
    for k in z:
        ans =  ans + str(k) + ' : ' + str(z[k]) + ' , '
    ans = ans + '}'
    print(ans)
    return(ans)


# query_components = { "imsi" : ["Hello"] }
PORT = 8007


def query_function( path):
    query_components = parse_qs(urlparse(path).query)
    counter = int( query_components["counter"][0])
    print(counter)
    #  do db query and return  html content
    ans =  uniqueness_query(counter)
    return(ans)

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>Title goes here.</title></head>")
        s.wfile.write("<body>")
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        #s.wfile.write("<p>You accessed path: %s</p>" % s.path)
	print(s.path)
        ans = query_function(s.path)
	print(ans)
        s.wfile.write(ans)
        s.wfile.write("</body></html>")


a = socketserver.TCPServer(("", PORT), MyHandler)
print("serving at port", PORT)
a.serve_forever()

