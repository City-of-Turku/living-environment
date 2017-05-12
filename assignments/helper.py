import urllib.error
import urllib.parse
import urllib.request

from assignments.exceptions import FeedbackSystemException


def post_to_feedback_system(url, data):
    data = urllib.parse.urlencode(data)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    try:
        urllib.request.urlopen(req)
    except urllib.error.URLError:
        raise FeedbackSystemException()
