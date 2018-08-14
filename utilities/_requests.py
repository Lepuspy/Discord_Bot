# -*- coding: utf-8 -*-
import requests


def get(url, params=None):
    r = requests.get(url, params=params)
    if r.status_code != 200:
        raise StatusError(f"HTTP ERROR status={r.status_code}")
    return r.json()

def post(url, params=None, headers=None):
    r = requests.post(url, params=params, headers=headers)
    if r.status_code != 200:
        raise StatusError(f"HTTP ERROR status={r.status_code}")
    return r.json()


class StatusError(Exception):pass