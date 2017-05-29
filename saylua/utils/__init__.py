from dateutil import tz

import time
import re
import string
import os
import random


def is_devserver():
    return os.environ['SERVER_SOFTWARE'].lower().startswith('development')


def get_gae_version():
    return os.environ['CURRENT_VERSION_ID']


def get_static_version_id():
    version = time.time()
    if not is_devserver():
        version = get_gae_version()
    return version


def pluralize(count, singular_noun, plural_noun=None):
    if not plural_noun:
        plural_noun = singular_noun + 's'
    if count == 1:
        return str(count) + ' ' + singular_noun
    return str(count) + ' ' + plural_noun


def saylua_time(time):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')
    time = time.replace(tzinfo=from_zone)
    return time.astimezone(to_zone)


def truncate(s, maxlen=50, placeholder='...'):
    if len(s) > maxlen:
        return (s[:maxlen] + placeholder)
    return s


def get_from_request(request, key, form_key=None, args_key=None):
    if not args_key:
        args_key = key
    if not form_key:
        form_key = key
    result = ''
    if form_key in request.form:
        result = request.form.get(form_key)
    elif request.args.get(args_key):
        result = request.args.get(args_key)
    return result


def random_token(length=32):
    choices = string.ascii_letters + string.digits
    return ''.join([random.SystemRandom().choice(choices) for _ in range(length)])


def canonize(name):
    name = re.sub(r'(\s|\W)+', '_', name)

    # Remove trailing characters from punctuation or elsewhere.
    name = name.strip('_-')
    return name.lower()
