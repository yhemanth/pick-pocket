import optparse
from commands.authorize_command import AuthorizeCommand


class PickPocket():
    def __init__(self):
        self.oauth_code_request = "http://getpocket.com/v3/oauth/request"
        self.access_code_request = "http://getpocket.com/v3/oauth/authorize"
        self.consumer_key = "37220-1449217af0d1fe41ecd0790b"
        self.web_redirect_url = "https://getpocket.com/connected_accounts"
        self.auth_request = "https://getpocket.com/auth/authorize?request_token={0}&redirect_uri=https://getpocket.com/connected_accounts"

    def authorize(self, options):
        command = AuthorizeCommand()
        command.execute(options)



if __name__ == "__main__":
    option_parser = optparse.OptionParser(prog="pick-pocket",
                                          description="A command line tool to query content in your Pocket account.")
    option_parser.add_option("-c", "--command", help="specify the command to run")
    option_parser.add_option("-C", "--config_file", help="file to store / read configuration from")
    (options, arguments) = option_parser.parse_args()
    pick_pocket = PickPocket()
    if options.command == "authorize":
        pick_pocket.authorize(options)
