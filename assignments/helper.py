import json
import urllib.error
import urllib.parse
import urllib.request

from django.utils.translation import gettext_lazy as _

from assignments.exceptions import FeedbackSystemException


def get_description_from_errors(errors):
    description = ''
    if isinstance(errors, list):
        description = ','.join(map(lambda error: error['description'], errors))
    elif isinstance(errors, dict):
        if 'description' in errors:
            description = errors['description']
        elif 'Message' in errors:
            description = errors['Message']
    return description


def post_to_feedback_system(url, data, api_key=None):
    data = urllib.parse.urlencode(data)
    data = data.encode('utf-8')
    try:
        req = urllib.request.Request(url, data)
        if api_key:
            req.add_header('apikey', api_key)
    except ValueError:
        raise FeedbackSystemException(_('Feedback system: please check if feedback system url is correctly set'))
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        charset = e.info().get_content_charset()
        content = e.read().decode(charset)
        errors = json.loads(content)
        description = get_description_from_errors(errors)
        raise FeedbackSystemException(_('Feedback system: ') + description)
    except urllib.error.URLError as e:
        raise FeedbackSystemException(_('Feedback system: ') + e.reason)
    else:
        return response.reason
