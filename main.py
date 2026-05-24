#!/usr/bin/env python3

"""
this script used to get data from ip-api.com
"""

import sys
import requests
import datetime
import psycopg2
import os
from dotenv import load_dotenv
from time import sleep

# you must procees a file path as a first argument
file_path = sys.argv[1]

# do not forget to prepare a file containing ip's
# one line -- one ip
# no headear, no sums

if file_path != None:
    with open(file_path) as file:
        for ip in file.read():

            n += 1

            # for free (and non-commencial usage) is allows to process 45 request per minute.
            sleep(1)

            print(f'#{n}: Processing {ip}')

            # this url got from ip-api.com
            # filed int is a combination of field to get
            url = f'http://ip-api.com/json/{ip}?fields=21745177'
            response = requests.get(url)

            print('Got response')
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

            # loading .env
            load_dotenv()
            

            conn = psycopg2.connect(
                host=os.getenv('HOST'),
                port=os.getenv('PORT'),
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWD')
            )

            try:
                with conn:
                    with conn.cursor() as cur:
                        cur.execute(query, data)
            
            except psycopg2.DatabaseError as e:
                conn.rollback()
                print(f'Database error: {e}')
                raise

            except Exception as e:
                conn.rollback()
                print(f'Unexpected error {e}')

            finally:
                conn.close()
                print('Done')











