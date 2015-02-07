import requests
from commands.common import Common


class SummarizeTagsCommand():

    def __init__(self):
        self.get_api = "http://getpocket.com/v3/get"

    def execute(self, options):
        config = open(options.config_file, 'r')
        access_token = filter(lambda l: l.startswith("access_token"), config.readlines())[0].strip().split(':')[1]
        response = requests.post(self.get_api,
                                 {'consumer_key': Common.consumer_key,
                                  'access_token': access_token,
                                  'state': 'all',
                                  'count': 5,
                                  'since': 1420054200,
                                  'detailType': 'complete'})
        print response.json()


