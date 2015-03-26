import argparse

from commands.authorize_command import AuthorizeCommand
from commands.fetch_command import FetchCommand
from commands.report_command import ReportCommand


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

    def fetch(self, options):
        command = FetchCommand()
        command.execute(options)

    def report(self, options):
        command = ReportCommand()
        command.execute(options)


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser(prog="pick-pocket",
                                              description="A command line tool to query content in your Pocket account.")
    subparsers = argument_parser.add_subparsers(dest='command')

    authorize_arg_parser = subparsers.add_parser('authorize', help='Authorize PickPocket application')
    authorize_arg_parser.add_argument("-A", "--auth_file", help="file to store/read authorization info from", required=True)

    fetch_arg_parser = subparsers.add_parser('fetch', help='fetch Pocket items')
    fetch_arg_parser.add_argument("-A", "--auth_file", help="file to store/read authorization info from", required=True)
    fetch_arg_parser.add_argument("-f", "--from_date",
                                  help="date past which modified items are fetched, format=YYYY-mm-dd", required=True)
    fetch_arg_parser.add_argument("-D", "--pocket_items_directory", help="directory where pocket items are stored", required=True)
    fetch_arg_parser.add_argument("-O", "--overwrite", help="overwrite existing pocket items", action='store_true')

    report_arg_parser = subparsers.add_parser('report', help='create a report on saved Pocket items')
    report_arg_parser.add_argument("-P", "--pocket_items_path", help="file/directory where pocket items are stored", required=True)

    options = argument_parser.parse_args()
    print options
    pick_pocket = PickPocket()
    if options.command == 'authorize':
        pick_pocket.authorize(options)
    elif options.command == 'fetch':
        pick_pocket.fetch(options)
    elif options.command == 'report':
        pick_pocket.report(options)
    else:
        argument_parser.print_help()