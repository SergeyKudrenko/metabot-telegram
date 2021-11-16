#%%
import os
import sys
import logging
from metabot.utils import Graph
from metabot.metabase import Client

logging.basicConfig(level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(name)s] %(message)s')
logger = logging.getLogger('metabot')


def get_config(config_name,
               default_value):
    try:
        value = os.environ[config_name]
    except:
        value = default_value
    finally:
        return value


if __name__ == '__main__':

    metabase_api_url=get_config('METABASE_API_URL', 'http://localhost:3000/api')
    username=get_config('METABASE_USERNAME', 'qwe@qwe.com')
    password=get_config('METABASE_PASSWORD', 'qwe123')

    metabase = Client(
        base_url=metabase_api_url,
        username=username,
        password=password
    )

    if not metabase.auth():
        sys.exit(os.EX_NOPERM)

    g = Graph()

    collection_id = metabase.get_collection_by_name(target='telegram')
    cards = metabase.get_cards(collection_id=collection_id)

    try:
        for c in cards:
            df = metabase.card_query(card_id=c['id'])
            g.plot(card=c, data=df)

            logger.info(f'{c["name"]}: {c["type"]}')
            logger.info(f'Data:\n{df}')

    except Exception as error:
        logger.error(f'Request failed with: {error}')

# %%
