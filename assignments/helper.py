import urllib.error
import urllib.parse
import urllib.request

from django.utils.translation import ugettext as _

from assignments.exceptions import FeedbackSystemException


def post_to_feedback_system(url, data):
    data = urllib.parse.urlencode(data)
    data = data.encode('utf-8')
    try:
        req = urllib.request.Request(url, data)
    except ValueError:
        raise FeedbackSystemException(_('Please check if feedback system url is correctly set'))
    try:
        urllib.request.urlopen(req)
    except urllib.error.URLError:
        raise FeedbackSystemException()
