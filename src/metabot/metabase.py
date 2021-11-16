import json
import logging
import requests
import pandas as pd

logger = logging.getLogger('metabase')

class Client(object):
    """ tbd """

    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password


    def auth(self):
        """ tbd """

        self.headers = {"Content-Type": "application/json"}
        payload = json.dumps({"username": self.username,
            "password": self.password}
        )

        try:
            resp = requests.post(f'{self.base_url}/session',
                headers=self.headers,
                data=payload
            )

            if resp.status_code==401:
                if len(json.loads(resp.text)['errors'])>0:
                    logger.fatal(
                        f'auth failed with {resp.status_code}: {resp.text}'
                    )
                return False

            token = json.loads(resp.text)["id"]
            self.headers["X-Metabase-Session"] = token
            return True

        except Exception as error:
            logger.error(f'auth failed with: {error}')


    def check_connection(func):
        """ Check auth token validity before sending requst """

        def wrapper(self, *args, **kwargs):
            try:
                resp = requests.get(f'{self.base_url}/login-history/current',
                    headers=self.headers
                )
                if resp.status_code==401:
                    self.auth()
            except Exception as error:
                logger.error(f'check_connection failed with: {error}')
            finally:
                return func(self, *args, **kwargs)
        return wrapper


    @check_connection
    def get_collection_by_name(self, target):
        """ tbd """
        try:
            resp = requests.get(f'{self.base_url}/collection/',
                headers=self.headers,
            )
            for c in json.loads(resp.text):
                if c['name'].lower() == target.lower():
                    return c['id']
        except Exception as error:
            logger.error(f'get_collection_by_name failed with: {error}')


    @check_connection
    def get_cards(self, collection_id):
        """ tbd """

        cards = []
        try:
            resp = requests.get(
                f'{self.base_url}/collection/{collection_id}/items',
                headers=self.headers,
            )
            for c in json.loads(resp.text)['data']:
                if c['model']=='card':
                    cards.append({"id": c['id'],
                        "name": c['name'],
                        "type": c['display']}
                    )
            return cards
        except Exception as error:
            logger.error(f'get_cards failed with: {error}')


    @check_connection
    def card_query(self, card_id):
        """ tbd """

        col_desc = []
        try:
            resp = requests.post(f'{self.base_url}/card/{card_id}/query',
                headers=self.headers,
            )
            ans = json.loads(resp.text)
            rows = ans['data']['rows']

            for i in ans['data']['results_metadata']['columns']:
                col_desc.append(i['display_name'])

            df = pd.DataFrame.from_dict(rows)
            df.columns = col_desc
            return df
        except Exception as error:
            logger.error(f'card_query failed with: {error}')
