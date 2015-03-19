from collections import OrderedDict
from datetime import datetime
import time

import requests

from commands.partitioner import Partitioner
import config
from commands.common import Common
from pocket_api import handle_api_failure


VALID = '0'


def parse(response):
    items = response['list']
    if len(items) == 0:
        return [], 0
    valid_items = map(lambda i: items[i], filter(lambda k: items[k]['status'] == VALID, items.keys()))
    return valid_items, len(items)


class FetchCommand():
    def __init__(self):
        self.get_api = "http://getpocket.com/v3/get"

    def __fetch_batch(self, access_token, cursor, from_date_ts, partitioner):
        item_count=0
        response = requests.post(self.get_api,
                                 json={'consumer_key': Common.consumer_key,
                                       'access_token': access_token,
                                       'state': 'all',
                                       'sort': 'oldest',
                                       'count': config.fetch_size,
                                       'offset': cursor,
                                       'since': from_date_ts,
                                       'detailType': 'complete'})
        if response.status_code == 200:
            items = response.json(object_pairs_hook=OrderedDict)
            (valid_items, item_count) = parse(items)
            for item in valid_items:
                partitioner.write(item)
            cursor += config.fetch_size
        else:
            handle_api_failure("Failed fetching items", response)
        return item_count, cursor

    def execute(self, options):
        partitioner = Partitioner(options.pocket_items_directory, options.overwrite)
        auth_config = open(options.auth_file, 'r')
        access_token = filter(lambda l: l.startswith("access_token"), auth_config.readlines())[0].strip().split(':')[1]
        from_date = datetime.strptime(options.from_date, '%Y-%m-%d').date()
        from_date_ts = time.mktime(from_date.timetuple())
        item_count, cursor = self.__fetch_batch(access_token, 0, from_date_ts, partitioner)
        while item_count == config.fetch_size:
            item_count, cursor = self.__fetch_batch(access_token, cursor, from_date_ts, partitioner)
