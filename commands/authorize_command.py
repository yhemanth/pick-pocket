import requests
import sys
from commands.common import Common
from pocket_api import handle_api_failure


class AuthorizeCommand():

    def __init__(self):
        self.oauth_code_request = "http://getpocket.com/v3/oauth/request"
        self.access_code_request = "http://getpocket.com/v3/oauth/authorize"
        self.web_redirect_url = "https://getpocket.com/connected_accounts"
        self.auth_request = "https://getpocket.com/auth/authorize?request_token={0}&redirect_uri=https://getpocket.com/connected_accounts"

    def execute(self, options):
        (access_token, user_name) = self.__begin_authorization()
        config = open(options.auth_file, 'w')
        config.write("access_token:{0}\n".format(access_token))
        config.write("user_name:{0}\n".format(user_name))
        config.close()
        print "pick-pocket is successfully authorized. Your access token is updated in ", options.auth_file

    def __begin_authorization(self):
        print "Step 1: Sending authorization request ..."
        response = requests.post(self.oauth_code_request,
                                 {'consumer_key': Common.consumer_key, 'redirect_uri': self.web_redirect_url})
        if response.status_code == 200:
            code = response.text.split("=")[1]
            print "Code: ", code
            print "Step 2: Authorize application by visiting your account's page: ", self.auth_request.format(code)
            print "When done, type 'Y' to continue. Else type 'N' to quit."
            auth_done = raw_input("Authorization done? [Y/N]:")
            if auth_done == 'Y':
                return self.__complete_authorization(code)
        else:
            handle_api_failure("Failed in authorization.", response)

    def __complete_authorization(self, code):
        print "Step 3: Getting authorization code ..."
        response = requests.post(self.access_code_request, {'consumer_key': Common.consumer_key, 'code': code})
        if response.status_code == 200:
            return self.__parse_access_code_response(response.text)
        else:
            handle_api_failure("Failed retrieving token.", response)

    def __parse_access_code_response(self, response_text):
        (access_token, user_name) = response_text.split('&')
        access_token = access_token.split("=")[1]
        user_name = user_name.split("=")[1]
        return (access_token, user_name)


