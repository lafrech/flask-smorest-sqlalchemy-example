"""Demonstration"""
# pylint: disable=invalid-name
import uuid
import datetime as dt
import json
import requests


DUMMY_ID = str(uuid.uuid4())

BASE_URL = 'http://127.0.0.1:5000/'
MEMBERS_URL = BASE_URL + 'members/'
TEAMS_URL = BASE_URL + 'teams/'

# GET list
ret = requests.get(MEMBERS_URL)
assert ret.status_code == 200
assert ret.json() == []


# POST
member_1 = {
    'first_name': 'Egon',
    'last_name': 'Spengler',
    'birthdate': dt.datetime(1958, 10, 2).isoformat()
}

ret = requests.post(MEMBERS_URL, data=json.dumps(member_1))
assert ret.status_code == 201
ret_val = ret.json()
member_1_id = ret_val.pop('id')
member_1_etag = ret.headers['ETag']
assert ret_val == member_1
member_1 = ret_val


# GET list
ret = requests.get(MEMBERS_URL)
assert ret.status_code == 200
ret_val = ret.json()
assert len(ret_val) == 1
assert ret_val[0]['id'] == member_1_id


# GET by id
ret = requests.get(MEMBERS_URL + member_1_id)
assert ret.status_code == 200
assert ret.headers['ETag'] == member_1_etag
ret_val = ret.json()
ret_val.pop('id')
assert ret_val == member_1


# PUT
del member_1['first_name']
ret = requests.put(
    MEMBERS_URL + member_1_id,
    data=json.dumps(member_1),
    headers={'If-Match': member_1_etag}
)
assert ret.status_code == 200
ret_val = ret.json()
ret_val.pop('id')
member_1_etag = ret.headers['ETag']
assert ret_val == member_1

# PUT wrong ID -> 404
ret = requests.put(
    MEMBERS_URL + DUMMY_ID,
    data=json.dumps(member_1),
    headers={'If-Match': member_1_etag}
)
assert ret.status_code == 404


# DELETE
ret = requests.delete(
    MEMBERS_URL + member_1_id,
    headers={'If-Match': member_1_etag}
)
assert ret.status_code == 204


# GET list
ret = requests.get(MEMBERS_URL)
assert ret.status_code == 200
assert ret.json() == []


# GET by id -> 404
ret = requests.get(MEMBERS_URL + member_1_id)
assert ret.status_code == 404

# GET list
ret = requests.get(TEAMS_URL)
assert ret.status_code == 200
assert ret.json() == []


# POST
team_1 = {
    'name': 'Ghostbusters',
}

ret = requests.post(TEAMS_URL, data=json.dumps(team_1))
assert ret.status_code == 201
ret_val = ret.json()
team_1_id = ret_val.pop('id')
team_1_etag = ret.headers['ETag']
assert ret_val == team_1
team_1 = ret_val
