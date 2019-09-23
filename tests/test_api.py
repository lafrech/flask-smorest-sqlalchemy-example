"""Demonstration"""
# pylint: disable=invalid-name
import datetime as dt
import json
import requests


BASE_URL = 'http://127.0.0.1:5000/'
MEMBERS_URL = BASE_URL + 'members/'


ret = requests.get(MEMBERS_URL)
assert ret.status_code == 200
assert ret.json() == []

member_1 = {
    'first_name': 'Egon',
    'last_name': 'Spengler',
    'birthdate': dt.datetime(1958, 10, 2).isoformat()
}

ret = requests.post(MEMBERS_URL, data=json.dumps(member_1))
assert ret.status_code == 201
ret_val = ret.json()
member_1_id = ret_val.pop('id')
assert ret_val == member_1
