#!/usr/bin/env python
#
#  This file was originally taken from:
#    https://smsaero.ru/api/class-python/
#
import hashlib
import json
import logging
import time
from datetime import datetime
from urllib.parse import urljoin

import requests


class SmsAeroError(Exception):
    """ Super class of all SmsAero Errors. """
    pass


class SmsAeroHTTPError(SmsAeroError):
    """ A Connection error occurred. """
    pass


class SmsAero(object):
    URL_GATE = 'https://gate.smsaero.ru/'
    SIGNATURE = 'NEWS'
    DIGITAL = 0
    TYPE_SEND = 2

    def __init__(self, user, passwd, url_gate=URL_GATE, signature=SIGNATURE,
                 digital=DIGITAL, type_send=TYPE_SEND):
        self.user = user
        self.url_gate = url_gate
        self.signature = signature
        self.digital = digital
        self.type_send = type_send
        self.session = requests.session()

        m = hashlib.md5()
        m.update(passwd.encode('utf-8'))
        self.passwd = m.hexdigest()

    def _request(self, selector, data):
        data.update({
            'user': self.user,
            'password': self.passwd,
            'answer': 'json',
        })
        url = urljoin(self.url_gate, selector)

        try:
            logging.getLogger().debug('POST: %s with data: %s', url, data)
            response = self.session.post(url, data=data)
        except requests.RequestException as err:
            raise SmsAeroHTTPError(err)

        if not response.status_code == 200:
            raise SmsAeroHTTPError('response status code is not 200')

        return self._check_response(response.content)

    def _check_response(self, content):
        try:
            response = json.loads(content.decode('utf-8'))
            if 'result' in response and response['result'] == u'reject':
                raise SmsAeroError(response['reason'])
            elif 'result' in response and response['result'] == u'no credits':
                raise SmsAeroError(response['result'])
            return response
        except ValueError:
            if 'incorrect language' in content:
                raise SmsAeroError("incorrect language in '...' use \
                    the cyrillic or roman alphabet.")
            else:
                raise SmsAeroError('unexpected format is received')

    def send(self, to, text, date=None, signature=None,
             digital=DIGITAL, type_send=TYPE_SEND):
        if signature is None:
            signature = self.signature

        data = {
            'from': signature,
            'digital': digital,
            'type_send': type_send,
            'to': to,
            'text': text,
        }

        if date is not None:
            if isinstance(date, datetime):
                data['date'] = int(time.mktime(date.timetuple()))
            else:
                raise SmsAeroError('param `date` is not datetime object')

        return self._request('/send/', data)
