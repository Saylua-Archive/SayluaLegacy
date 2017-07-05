from dateutil import tz
from urlparse import urlparse, urljoin
from flask import request, redirect, url_for

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


def format_number(n):
    return "{:,}".format(n)


def int_or_none(n):
    try:
        n = int(n)
        return n
    except:
        return None


def pluralize(count, singular_noun, plural_noun=None):
    if not plural_noun:
        plural_noun = singular_noun + 's'
    if count == 1:
        return format_number(count) + ' ' + singular_noun
    return format_number(count) + ' ' + plural_noun


def add_article(singular_noun):
    vowels = ("a", "e", "i", "o", "u")
    if singular_noun.startswith(vowels):
        return "an " + singular_noun
    else:
        return "a " + singular_noun


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


# http://flask.pocoo.org/snippets/62/
def is_safe_url(target):
    if not target:
        return False
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.form.get('next'), request.values.get('next'), request.referrer:
        if is_safe_url(target):
            return target
    return ''


def redirect_to_referer(endpoint='general.home', **values):
    if is_safe_url(request.referrer):
        return redirect(request.referrer)
    return redirect(url_for(endpoint, **values))


def random_token(length=32):
    choices = string.ascii_letters + string.digits
    return ''.join([random.SystemRandom().choice(choices) for _ in range(length)])


def canonize(name):
    name = re.sub(r'(\s|\W)+', '_', name)

    # Remove trailing characters from punctuation or elsewhere.
    name = name.strip('_-')
    return name.lower()


def go_up_path(n, path):
    if n <= 0:
        return path
    else:
        return go_up_path(n - 1, os.path.dirname(path))
