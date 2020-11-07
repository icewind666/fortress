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

HOST_NAME = '194.1.239.148'  # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 9999  # Maybe set this to 9000.
TEMP_FILE = 'temp.txt'


def write_to_db(dt, value, sensor):
    try:
        connection = psycopg2.connect(user="steelrat",
                                      password="steelrat_password",
                                      host="localhost",
                                      port="5432",
                                      database="fortress")

        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO temperature (dt, value, sensor) VALUES (%s,%s,%s)"""
        record_to_insert = (dt, value, sensor)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()


def write_humidity_to_db(dt, value, sensor):
    try:
        connection = psycopg2.connect(user="steelrat",
                                      password="steelrat_password",
                                      host="localhost",
                                      port="5432",
                                      database="fortress")

        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO humidity (dt, value, sensor) VALUES (%s,%s,%s)"""
        record_to_insert = (dt, value, sensor)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()


def get_archive_from_db():
    con = sqlite3.connect('temp')
    cur = con.cursor()
    cur.execute('select dt,value,sensor from (select * from temperature order by id DESC limit 10) order by id ASC;')

    result = []

    for row in cur:
        dt = row[0]
        value = row[1]
        sensor = row[2]

        pair = {"dt": dt, "value": value, "sensor": sensor}
        result.append(pair)

    result_json = json.dumps(result)
    con.close()
    return result_json


def write_to_storage(x, sensor):
    dt = datetime.datetime.now()
    write_to_db(dt, x, sensor)


def write_to_humidity_storage(x, sensor):
    dt = datetime.datetime.now()
    write_humidity_to_db(dt, x, sensor)


class MyHandler(BaseHTTPRequestHandler):

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

    def do_POST(s):
        url = s.path
        if "json" in url:
            # call data json from db
            s.get_json_from_db()
        else:
            content_length = int(s.headers['Content-Length'])
            post_data = s.rfile.read(content_length)
            post_data = post_data.decode('utf-8')

            query_parsed = parse_qs(post_data)

            value = float(query_parsed['value'][0])
            sensor_id = str(query_parsed['sensor_id'][0])

            if sensor_id == "HUMIDITY":
                write_to_humidity_storage(value, "room_h")

            if sensor_id == "DS18B20":
                write_to_storage(value, "room_t")
            if sensor_id == "kitchen":
                write_to_storage(value, "kitchen_t")
            if sensor_id == "garden":
                write_to_storage(value, "garden_t")

            print("Request {}".format(post_data))
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

