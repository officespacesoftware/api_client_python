import datetime
import requests
import json
import argparse
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
from lib.oss_api_config import OfficeSpaceConf

conf = OfficeSpaceConf('conf/oss_creds.json')

arg_parser = argparse.ArgumentParser(description='Move a person by email and phone MAC address.', usage='milton@initech.com -in ABCDEF02 -out ABCDEF01')
arg_parser.add_argument('email')
arg_parser.add_argument('-in-MAC', '-in')
arg_parser.add_argument('-out-MAC', '-out')
args = arg_parser.parse_args()
if not args.in_MAC and not args.out_MAC:
    arg_parser.error('Either a login or logout MAC must be specified')

db = TinyDB(conf.DB_PATH)
table_seats = db.table('seats')
table_macs_to_seats = db.table('macs_to_seats')

EMPLOYEE_EMAIL = args.email
LOGIN_MAC = args.in_MAC
LOGOUT_MAC = args.out_MAC

to_seat_id = 0
if (len(table_macs_to_seats.search(Query().mac == LOGIN_MAC)) > 0):
    to_seat_id = table_macs_to_seats.search(Query().mac == LOGIN_MAC)[0]['seat']

from_seat_id = 0
if (len(table_macs_to_seats.search(Query().mac == LOGOUT_MAC)) > 0):
    from_seat_id = table_macs_to_seats.search(Query().mac == LOGOUT_MAC)[0]['seat']

move_body = {'employee_id': EMPLOYEE_EMAIL.split('@', 1)[0],
             'move_time': str(datetime.datetime.now().replace(microsecond=0)),
             'scheduled_by': 'Phone Login Integration'}

if (from_seat_id <= 0 and to_seat_id <= 0):
    exit('There must be at least one matching MAC address.')

if (to_seat_id > 0):
    move_body['to_seat_id'] = to_seat_id

if (from_seat_id > 0):
    move_body['from_seat_id'] = from_seat_id

print(move_body)

response = requests.post(conf.URL_BASE + conf.URL_MOVES, headers=conf.HEADERS, data=json.dumps(move_body))
if (response.status_code < 200 or response.status_code >= 300):
    exit('OfficeSpace API returned an error code: ' + str(response.status_code) + ' ' + response.reason)

move_id = json.loads(response.text)['response']['id']

response = requests.put(conf.URL_BASE + conf.URL_MOVES + '/' + str(move_id) + '/complete', headers=conf.HEADERS)

print(str(response.status_code) + ': ' + response.reason)