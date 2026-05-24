#!/usr/bin/env python3

"""
this script used to get data from ip-api.com
"""

import sys
import requests
import datetime
import psycopg2
import os
import dotenv

# you must procees a file path as a first argument
file_path = sys.argv[1]

# do not forget to prepare a file containing ip's
# one line -- one ip
# no headear, no sums

if file_path != None:
    with open(file_path) as file:
        for ip in file.read():

            # this url got from ip-api.com
            # for free (and non-commencial usage) is allows to process 45 request per minute.
            # filed int is a combination of field to get
            url = f'http://ip-api.com/json/{ip}?fields=21745177'
            response = requests.get(url)

            data = response.json()

            # in the response there is no ip address, so we add it maunally
            data["ip": ip]

            # we suppose to keep data in db, so we need a date in order to update it if it was updated a long ago
            date = datetime.datetime.now().date()

            # we do not need status field in db
            data.pop('status')

            # preparing data to proceed
            columns = ", ".join(data.keys())
            placeholders = ", ".join([f"%({key})s" for key in data.keys()])

            # preparing a sql-request
            query = f"""
                INSERT INTO ip_geolocation ({columns})
                VALUES ({placeholders})
            """

            # 

            conn = psycopg2.connect(
                host="5.35.112.175",
                port=55432,
                dbname="cowrie",
                user="cowrie",
                password="changeme"
            )











