from datetime import datetime, date
import time
import requests
from commands.common import Common


class FetchCommand():

    def execute(self, options):
        config = open(options.config_file, 'r')
        start_date_ts = time.mktime(datetime.strptime(options.start_date, '%Y-%m-%d').timetuple())
        access_token = filter(lambda l: l.startswith("access_token"), config.readlines())[0].strip().split(':')[1]
        response = requests.post(Common.get_api,
                                 {'consumer_key': Common.consumer_key,
                                  'access_token': access_token,
                                  'state': 'all',
                                  'sort': 'oldest',
                                  'count': 10,
                                  #'since': start_date_ts,
                                  'detailType': 'complete',
                                  'offset': 10})
        self.parse(response.json())

    def parse(self, response):
        item_ids = response['list'].keys()
        print "url|time_added|time_updated"
        for item_id in item_ids:
            item = response['list'][item_id]
            print item['resolved_url'], "|", date.fromtimestamp(float(item['time_added'])), \
                "|", date.fromtimestamp(float(item['time_updated']))
