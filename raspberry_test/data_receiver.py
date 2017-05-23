#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import Libraries
import os
import glob
import json
import time
import sqlite3
import datetime
import BaseHTTPServer
from urlparse import urlparse, parse_qs

HOST_NAME = '192.168.0.104' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 9999 # Maybe set this to 9000.
TEMP_FILE = 'temp.txt'

def write_to_db(dt, value):
    con = sqlite3.connect('temp')
    cur = con.cursor()
    cur.execute('INSERT INTO temperature (id, dt, value) VALUES(NULL, ?, ?)', (dt, value))
    con.commit()
    con.close()

def get_last_from_db():
    con = sqlite3.connect('temp')
    cur = con.cursor()
    cur.execute('SELECT value FROM temperature ORDER by dt DESC')
    data = cur.fetchone()
    result = data[0]
    #print result
    con.close()
    return result

def get_archive_from_db():
    #print 'get_archive_from_db()'
    con = sqlite3.connect('temp')
    cur = con.cursor()
    cur.execute('select dt,value from (select * from temperature order by id DESC limit 50) order by id ASC;')

    result = []

    for row in cur:
        dt = row[0]
        value = row[1]

        pair = {"dt":dt, "value":value}
        result.append(pair)

    result_json = json.dumps(result)
    #print result_json
    con.close()
    return result_json



def write_to_storage(x):
    dt = datetime.datetime.now()
    #date_str = dt.strftime("%Y.%m.%dT%I:%M:%S")
    write_to_db(dt, x)

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.send_header("Access-Control-Allow-Origin", "*")
        s.end_headers()

    def get_json_from_db(s):
        s.send_response(200)
        s.send_header("Access-Control-Allow-Origin", "*")
        s.send_header("Content-type", "application/json")
        s.end_headers()

        json_str = get_archive_from_db()

        s.wfile.write(json_str)


    def do_GET(s):
        url = s.path
        #print url
        if "json" in url:
            # call data json from db
            s.get_json_from_db()
        else:
            query_parsed = parse_qs(urlparse(url).query)

            temperature = float(query_parsed['t'][0])
            last_value = get_last_from_db()
            if abs(temperature - last_value) > 0.5:
                #print "T=", temperature, "; LAST=", last_value
                #print "Writing new value"
                write_to_storage(temperature)

            """Respond to a GET request."""
            s.send_response(200)
            s.send_header("Content-type", "text/html")
            s.end_headers()
            s.wfile.write("<html><head><title>Title goes here.</title></head>")
            s.wfile.write("<body><p>This is a test.</p>")
            s.wfile.write("<p>You accessed path: %s</p>" % s.path)
            s.wfile.write("</body></html>")


if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

