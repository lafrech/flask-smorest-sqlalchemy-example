# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # flask-smorest-sqlalchemy demo

# Demonstrates the use of the flask-smorest + sqlalchemy example

import uuid
import datetime as dt
import json
import requests


DUMMY_ID = str(uuid.uuid4())
DUMMY_ETAG = 40 * '0'

BASE_URL = 'http://127.0.0.1:5000/'
MEMBERS_URL = BASE_URL + 'members/'
TEAMS_URL = BASE_URL + 'teams/'

for member in requests.get(MEMBERS_URL).json():
    etag = requests.get(MEMBERS_URL + member['id']).headers['ETag']
    requests.delete(MEMBERS_URL + member['id'], headers={'If-Match': etag})
for team in requests.get(TEAMS_URL).json():
    etag = requests.get(TEAMS_URL + team['id']).headers['ETag']
    requests.delete(TEAMS_URL + team['id'], headers={'If-Match': etag})

# ---------------------------------------------------------------------------

# ## GET members list

ret = requests.get(MEMBERS_URL)


ret.status_code

ret.json()

ret.headers['X-Pagination']

ret.headers['ETag']

# ## POST a member

member_1 = {
    'first_name': 'Egon',
    'last_name': 'Spengler',
    'birthdate': dt.datetime(1958, 10, 2).isoformat()
}

ret = requests.post(
    MEMBERS_URL,
    data=json.dumps(member_1)
)


ret.status_code

ret.json()

ret.headers['Etag']

member_1_id = ret.json()['id']

# ## GET members list

ret = requests.get(MEMBERS_URL)


ret.status_code

ret.json()

ret.headers['X-Pagination']

ret.headers['ETag']

# ## GET member by ID

ret = requests.get(MEMBERS_URL + member_1_id)


ret.status_code

ret.json()

ret.headers['ETag']

member_1_etag = ret.headers['ETag']

# ## GET member by ID, not modified

ret = requests.get(
    MEMBERS_URL + member_1_id,
    headers={'If-None-Match': member_1_etag}
)

ret.status_code

ret.text

# ## PUT member

del member_1['first_name']
ret = requests.put(
    MEMBERS_URL + member_1_id,
    data=json.dumps(member_1),
    headers={'If-Match': member_1_etag}
)

ret.status_code

ret.json()

ret.headers['ETag']

member_1_etag = ret.headers['ETag']

# ## PUT member, missing ETag

ret = requests.put(
    MEMBERS_URL + member_1_id,
    data=json.dumps(member_1),
)
ret.status_code

# ## PUT member, wrong ETag

ret = requests.put(
    MEMBERS_URL + member_1_id,
    data=json.dumps(member_1),
    headers={'If-Match': DUMMY_ETAG}
)
ret.status_code

# ## PUT member, wrong ID

ret = requests.put(
    MEMBERS_URL + DUMMY_ID,
    data=json.dumps(member_1),
    headers={'If-Match': member_1_etag}
)
ret.status_code


# ## DELETE member

ret = requests.delete(
    MEMBERS_URL + member_1_id,
    headers={'If-Match': member_1_etag}
)
ret.status_code


# # GET members list

ret = requests.get(MEMBERS_URL)
ret.json()


# ## GET member by id -> 404

ret = requests.get(MEMBERS_URL + member_1_id)
ret.status_code

# ---------------------------------------------------------------------------

# ## GET teams list

ret = requests.get(TEAMS_URL)
ret.json()


# ## POST teams

team_1 = {
    'name': 'Ghostbusters',
}
ret = requests.post(
    TEAMS_URL,
    data=json.dumps(team_1)
)
team_1_id = ret.json().pop('id')

team_2 = {
    'name': 'A-Team',
}
ret = requests.post(
    TEAMS_URL,
    data=json.dumps(team_2)
)
team_2_id = ret.json().pop('id')


# ## POST members with teams

member_1 = {
    'first_name': 'Egon',
    'last_name': 'Spengler',
    'birthdate': dt.datetime(1958, 10, 2).isoformat(),
    'team_id': team_1_id,
}
ret = requests.post(
    MEMBERS_URL,
    data=json.dumps(member_1)
)
member_1_id = ret.json().pop('id')

member_2 = {
    'first_name': 'Peter',
    'last_name': 'Venkman',
    'birthdate': dt.datetime(1960, 9, 6).isoformat(),
    'team_id': team_1_id,
}
ret = requests.post(
    MEMBERS_URL,
    data=json.dumps(member_1)
)
member_2_id = ret.json().pop('id')

# ## GET members with team filter

ret = requests.get(
    MEMBERS_URL,
    params={'team_id': team_1_id}
)
ret.json()

ret = requests.get(
    MEMBERS_URL,
    params={'team_id': team_2_id}
)
ret.json()

# ## GET teams with member filter

ret = requests.get(
    TEAMS_URL,
    params={'member_id': member_1_id}
)
ret.json()

ret = requests.get(
    TEAMS_URL,
    params={'member_id': member_2_id}
)
ret.json()
