#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

# filename   : utils.py
# created at : 2013-02-17 09:37:31
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'

import dns
import dns.exception
import dns.tsig
import dns.tsigkeyring
import dns.update
import dns.query

DDNS_TTL = 60


class NSUpdateError(Exception):
    pass


def keyring_from_string(s):
    k = {s.rsplit(' ')[0]: s.rsplit(' ')[1]}
    try:
        return dns.tsigkeyring.from_text(k)
    except Exception as e:
        raise NSUpdateError('key "%s" is not a valid key. (%s)' % (s, e))


def ddns_update(entry):

    zone = entry.zone.name
    key = keyring_from_string(entry.zone.key)
    server = entry.zone.master_server
    domain = entry.domainname.encode('UTF-8')

    if entry.record_a:
        payload = entry.record_a.encode('UTF-8')
        ddns_update_entry(domain, 'A', payload, zone, key, server)

    if entry.record_aaaa:
        payload = entry.record_aaaa.encode('UTF-8')
        ddns_update_entry(domain, 'AAAA', payload, zone, key, server)


def ddns_update_entry(domain, record_type, payload, zone, key, server):

    try:
        updater = dns.update.Update(zone, keyring=key)
        updater.delete(domain, record_type)
        updater.add(domain, DDNS_TTL, record_type, payload)
        response = dns.query.tcp(updater, server)

        return response
    except dns.exception.SyntaxError as e:
        raise NSUpdateError('payload syntax error: %s' % e)
    except dns.tsig.PeerBadKey:
        raise NSUpdateError('key is refused')
