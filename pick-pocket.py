import urllib
import sys
from urlparse import parse_qsl


class PickPocket():
    def __init__(self):
        self.oauth_code_request = "http://getpocket.com/v3/oauth/request"
        self.auth_request = "http://getpocket.com/v3/oauth/authorize"
        self.consumer_key = "37220-1449217af0d1fe41ecd0790b"
        self.web_redirect_url = "https://getpocket.com/connected_accounts"

    def build_post_args(self, request_options_map):
        data = urllib.urlencode(request_options_map)
        data.encode('UTF-8')
        return data

    def authorize(self):
        data = self.build_post_args({'consumer_key': self.consumer_key, 'redirect_uri': self.web_redirect_url})
        oauth_response = urllib.urlopen(self.oauth_code_request, data)
        if oauth_response.getcode() == 200:
            code = oauth_response.readline().split("=")[1]
        oauth_response.close()
        print "Code: ", code

    def get_access_token(self, code):
        data = self.build_post_args({'consumer_key': self.consumer_key, 'code': code})
        access_token_response = urllib.urlopen(self.auth_request, data)
        print access_token_response.getcode()
        if access_token_response.getcode() == 200:
            results = parse_qsl(access_token_response.readline())
            for result in results:
                print result
        else:
            print access_token_response.info()

if __name__ == "__main__":
    pick_pocket = PickPocket()
    if len(sys.argv) == 2:
        pick_pocket.get_access_token(sys.argv[1])
    else:
        pick_pocket.authorize()