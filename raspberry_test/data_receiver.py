#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import Libraries
import os
import glob
import json
import time
import sqlite3
import datetime
import psycopg2
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

HOST_NAME = 'localhost'  # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 9999  # Maybe set this to 9000.
TEMP_FILE = 'temp.txt'


def write_to_db(dt, value):
    try:
        connection = psycopg2.connect(user="steelrat",
                                      password="steelrat_password",
                                      host="localhost",
                                      port="5432",
                                      database="steelrat")

        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO temperature (dt, value) VALUES (%s,%s)"""
        record_to_insert = (dt, value)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into temperature table")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def write_humidity_to_db(dt, value):
    try:
        connection = psycopg2.connect(user="steelrat",
                                      password="steelrat_password",
                                      host="localhost",
                                      port="5432",
                                      database="steelrat")

        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO humidity (dt, value) VALUES (%s,%s)"""
        record_to_insert = (dt, value)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into humidity table")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")



def write_to_storage(x):
    dt = datetime.datetime.now()
    write_to_db(dt, x)


def write_to_humidity_storage(x):
    dt = datetime.datetime.now()
    write_humidity_to_db(dt, x)


class MyHandler(BaseHTTPRequestHandler):

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.send_header("Access-Control-Allow-Origin", "*")
        s.end_headers()

    def get_json_from_db(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-type", "application/json")
        self.end_headers()

        json_str = get_archive_from_db()

        self.wfile.write(json_str)

    def do_POST(s):
        url = s.path
        if "json" in url:
            # call data json from db
            self.get_json_from_db()
        else:
            content_length = int(s.headers['Content-Length'])
            post_data = s.rfile.read(content_length)
            post_data = post_data.decode('utf-8')

            query_parsed = parse_qs(post_data)

            value = float(query_parsed['value'][0])
            sensor_id = str(query_parsed['sensor_id'][0])
            #last_humidity_value = get_last_humidity_from_db()
            #last_temp_value = get_last_temp_from_db()

            if sensor_id == "HUMIDITY":
                #if abs(value - last_humidity_value) > 0.1:
                write_to_humidity_storage(value)
                #print("humidity = " + str(value))

            if sensor_id == "DS18B20":
                # if abs(value - last_temp_value) > 0.1:
                write_to_storage(value)
#                    print("temperature = " + str(value))

            s.wfile.write("POST request for {}".format(s.path).encode('utf-8'))


if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))

