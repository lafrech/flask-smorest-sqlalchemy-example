"""API tests"""
# pylint: disable=invalid-name
import uuid
import datetime as dt
import json


DUMMY_ID = str(uuid.UUID('00000000-0000-0000-0000-000000000000'))

MEMBERS_URL = '/members/'
TEAMS_URL = '/teams/'


class TestApi:

    def test_members_api(self, app):

        client = app.test_client()

        # GET list
        ret = client.get(MEMBERS_URL)
        assert ret.status_code == 200
        assert ret.json == []

        # POST
        member_1 = {
            'first_name': 'Egon',
            'last_name': 'Spengler',
            'birthdate': dt.datetime(1958, 10, 2).isoformat()
        }

        ret = client.post(MEMBERS_URL, data=json.dumps(member_1))
        assert ret.status_code == 201
        ret_val = ret.json
        member_1_id = ret_val.pop('id')
        member_1_etag = ret.headers['ETag']
        assert ret_val == member_1

        # GET list
        ret = client.get(MEMBERS_URL)
        assert ret.status_code == 200
        ret_val = ret.json
        assert len(ret_val) == 1
        assert ret_val[0]['id'] == member_1_id

        # GET by id
        ret = client.get(MEMBERS_URL + member_1_id)
        assert ret.status_code == 200
        assert ret.headers['ETag'] == member_1_etag
        ret_val = ret.json
        ret_val.pop('id')
        assert ret_val == member_1

        # PUT
        del member_1['first_name']
        ret = client.put(
            MEMBERS_URL + member_1_id,
            data=json.dumps(member_1),
            headers={'If-Match': member_1_etag}
        )
        assert ret.status_code == 200
        ret_val = ret.json
        ret_val.pop('id')
        member_1_etag = ret.headers['ETag']
        assert ret_val == member_1

        # PUT wrong ID -> 404
        ret = client.put(
            MEMBERS_URL + DUMMY_ID,
            data=json.dumps(member_1),
            headers={'If-Match': member_1_etag}
        )
        assert ret.status_code == 404

        # DELETE
        ret = client.delete(
            MEMBERS_URL + member_1_id,
            headers={'If-Match': member_1_etag}
        )
        assert ret.status_code == 204

        # GET list
        ret = client.get(MEMBERS_URL)
        assert ret.status_code == 200
        assert ret.json == []

        # GET by id -> 404
        ret = client.get(MEMBERS_URL + member_1_id)
        assert ret.status_code == 404

    def test_teams_members_relations(self, app):

        client = app.test_client()

        # GET list
        ret = client.get(TEAMS_URL)
        assert ret.status_code == 200
        assert ret.json == []

        # POST
        team_1 = {
            'name': 'Ghostbusters',
        }

        ret = client.post(TEAMS_URL, data=json.dumps(team_1))
        assert ret.status_code == 201
        ret_val = ret.json
        team_1_id = ret_val.pop('id')
        assert ret_val == team_1

        # POST
        team_2 = {
            'name': 'A-Team',
        }

        ret = client.post(TEAMS_URL, data=json.dumps(team_2))
        assert ret.status_code == 201
        ret_val = ret.json
        team_2_id = ret_val.pop('id')
        assert ret_val == team_2

        # POST
        member_1 = {
            'first_name': 'Egon',
            'last_name': 'Spengler',
            'birthdate': dt.datetime(1958, 10, 2).isoformat(),
            'team_id': team_1_id,
        }
        ret = client.post(MEMBERS_URL, data=json.dumps(member_1))
        assert ret.status_code == 201
        ret_val = ret.json
        member_1_id = ret_val.pop('id')

        member_2 = {
            'first_name': 'Peter',
            'last_name': 'Venkman',
            'birthdate': dt.datetime(1960, 9, 6).isoformat(),
            'team_id': team_1_id,
        }
        ret = client.post(MEMBERS_URL, data=json.dumps(member_2))
        assert ret.status_code == 201
        ret_val = ret.json
        member_2_id = ret_val.pop('id')

        # GET teams with member_id filter
        ret = client.get(TEAMS_URL, query_string={'member_id': member_1_id})
        assert ret.status_code == 200
        ret_val = ret.json
        assert len(ret_val) == 1
        assert ret_val[0]['id'] == team_1_id

        # GET members with team_id filter: team 1
        ret = client.get(MEMBERS_URL, query_string={'team_id': team_1_id})
        assert ret.status_code == 200
        ret_val = ret.json
        assert len(ret_val) == 2
        assert set(v['id'] for v in ret_val) == {member_1_id, member_2_id}

        # GET members with team_id filter: team 2
        ret = client.get(MEMBERS_URL, query_string={'team_id': team_2_id})
        assert ret.status_code == 200
        ret_val = ret.json
        assert len(ret_val) == 0
