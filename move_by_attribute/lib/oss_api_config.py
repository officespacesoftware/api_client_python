import json

class OfficeSpaceConf(object):

    def __init__(self, creds_file):
        ''' loads credentials file

        Args:
            credsfile (str): json configuration file

        '''
        with open(creds_file) as json_file:
            config = json.load(json_file)

            self.DOMAIN = config.get('domain')
            self.API_KEY = config.get('api_key')
            self.DB_PATH = config.get('db_path')
            self.ATTRIBUTE_NAME = config.get('attribute_name')
            self.URL_BASE = 'https://' + self.DOMAIN
            self.URL_EMPLOYEES = '/api/1/employees?client_employee_id='
            self.URL_MOVES = '/api/1/moves'
            self.URL_SEATS = '/api/1/seats'
            self.URL_ATTRIBUTES = '/attributes'
            self.HEADERS = {
                'Authorization': 'Token token=' + self.API_KEY,
                'Content-Type': 'application/json; charset=utf-8'
                }