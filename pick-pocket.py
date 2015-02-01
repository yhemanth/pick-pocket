import optparse
import requests
import sys


class PickPocket():
    def __init__(self):
        self.oauth_code_request = "http://getpocket.com/v3/oauth/request"
        self.access_code_request = "http://getpocket.com/v3/oauth/authorize"
        self.consumer_key = "37220-1449217af0d1fe41ecd0790b"
        self.web_redirect_url = "https://getpocket.com/connected_accounts"
        self.auth_request = "https://getpocket.com/auth/authorize?request_token={0}&redirect_uri=https://getpocket.com/connected_accounts"

    def authorize(self, options):
        (access_token, user_name) = self.__begin_authorization()
        config = open(options.config_file, 'w')
        config.write("access_token:{0}\n".format(access_token))
        config.write("user_name:{0}\n".format(user_name))
        config.close()

    @staticmethod
    def __handle_auth_failure(message, response):
        print message
        print "Status code: ", response.status_code
        print "Additional info, X-Error-Code: ", response.headers['X-Error-Code']
        print "Additional info, X-Error: ", response.headers['X-Error']
        sys.exit(-1)

    def __begin_authorization(self):
        print "Step 1: Sending authorization request ..."
        response = requests.post(self.oauth_code_request,
                                 {'consumer_key': self.consumer_key, 'redirect_uri': self.web_redirect_url})
        if response.status_code == 200:
            code = response.text.split("=")[1]
            print "Code: ", code
            print "Step 2: Authorize application by visiting your account's page: ", self.auth_request.format(code)
            print "When done, type 'Y' to continue. Else type 'N' to quit."
            auth_done = raw_input("Authorization done? [Y/N]:")
            if auth_done == 'Y':
                return self.__complete_authorization(code)
        else:
            self.__handle_auth_failure("Failed in authorization.", response)

    def __complete_authorization(self, code):
        print "Step 3: Getting authorization code ..."
        response = requests.post(self.access_code_request, {'consumer_key': self.consumer_key, 'code': code})
        if response.status_code == 200:
            return self.__parse_access_code_response(response.text)
        else:
            self.__handle_auth_failure("Failed retrieving token.", response)

    def __parse_access_code_response(self, response_text):
        (access_token, user_name) = response_text.split('&')
        access_token = access_token.split("=")[1]
        user_name = user_name.split("=")[1]
        return (access_token, user_name)


if __name__ == "__main__":
    option_parser = optparse.OptionParser(prog="pick-pocket",
                                          description="A command line tool to query content in your Pocket account.")
    option_parser.add_option("-c", "--command", help="specify the command to run")
    option_parser.add_option("-C", "--config_file", help="file to store / read configuration from")
    (options, arguments) = option_parser.parse_args()
    pick_pocket = PickPocket()
    if options.command == "authorize":
        pick_pocket.authorize(options)
