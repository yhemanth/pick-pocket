import sys


@staticmethod
def handle_api_failure(message, response):
    print message
    print "Status code: ", response.status_code
    print "Additional info, X-Error-Code: ", response.headers['X-Error-Code']
    print "Additional info, X-Error: ", response.headers['X-Error']
    sys.exit(-1)
