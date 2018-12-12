import requests
import json
from tinydb import TinyDB, Query
from lib.oss_api_config import OfficeSpaceConf

conf = OfficeSpaceConf('conf/oss_creds.json')

db = TinyDB(conf.DB_PATH)
db.purge_tables()
table_seats = db.table('seats')
table_macs_to_seats = db.table('macs_to_seats')

response = requests.request("GET", conf.URL_BASE + conf.URL_SEATS, headers=conf.HEADERS)
table_seats.insert_multiple(json.loads(response.text).get("response"))

Eligible_Seats = Query()

for seat in table_seats.search((Eligible_Seats.online == True) 
                                & (Eligible_Seats.hot_desk == False) 
                                & (Eligible_Seats.utility == -1)):
    response = requests.request("GET", conf.URL_BASE + seat['room_url'] + conf.URL_ATTRIBUTES, headers=conf.HEADERS)
    attributes = json.loads(response.text).get("response")

    for attribute in attributes:
        if (attribute['name'] == conf.ATTRIBUTE_NAME):
                table_macs_to_seats.insert({'mac': attribute['value'], 'seat': seat['id']})

print(table_macs_to_seats.all())
